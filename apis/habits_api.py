from flask_restplus import Namespace, Resource, fields
from models.habits import HabitModel

from models.authorization import authorize_decorator
hm = HabitModel()

api = Namespace('habits', description='Habit api')


habit = api.model(name='habit', model={
    'body': fields.String(description='The habit text.'),
    'keywords': fields.List(fields.String('Keyword')),
    'repetition': fields.Integer('Weekly repetition goal, e.g 1, 7'),
    'key': fields.String('Entity key')
})


# def store_habit(habit):
#     client = datastore.Client()
#     text = habit['body']
#     habit_key = client.key('habit', str(
#         base64.b64encode(text.encode('utf-8')), 'utf-8'))
#     habit_entity = datastore.Entity(habit_key)
#     habit_entity.update(habit)
#     client.put(habit_entity)
#     return {'id': habit_entity.key.id}


# def get_habits(limit=20):
#     habits_list = []
#     client = datastore.Client()
#     query = client.query(kind='habit')
#     habits = query.fetch(limit=limit)
#     for habit in habits:
#         habit['id'] = habit.key.id_or_name
#         habits_list.append(habit)
#     return habits_list


# def get_habit(id):
#     client = datastore.Client()
#     key = client.key('habit', id)
#     habit = client.get(key)
#     habit['id'] = key.id
#     return habit


# def delete_habit(id):
#     client = datastore.Client()
#     key = client.key('habit', id)
#     client.delete(key)
#     return {'success': True}


# def get_habit_keys_only():
#     client = datastore.Client()
#     query = client.query(kind='habit')
#     query.keys_only()
#     res = query.fetch()
#     return res


# def get_habit_keys():
#     habits = get_habit_keys_only()
#     return [ent.key.id_or_name for ent in habits]


# def delete_all_habits():
#     habits = get_habit_keys_only()
#     habit_keys = [ent.key for ent in habits]
#     client = datastore.Client()
#     client.delete_multi(habit_keys)
#     return {'success': True}


@api.route('')
class Habit(Resource):
    method_decorators = [authorize_decorator]
    @api.expect(habit, validate=False)
    @api.response(200, 'Success', habit)
    def post(self):
        habit = api.payload
        key_id = hm.store_habit(habit)
        habit['id'] = key_id
        return habit

    @api.response(200, 'Success', [habit])
    def get(self):
        habits = hm.get_habits()
        return habits

    def delete(self):
        res = hm.delete_all_habits()
        return res


@api.route('/<int:id>')
class OneHabit(Resource):
    method_decorators = [authorize_decorator]

    def get(self, id):
        habit = hm.get_habit(id)
        if habit is None:
            return {}, 404
        return habit, 200

    def delete(self, id):
        result = hm.delete_habit(id)
        return result


@api.route('/keys')
class GetHabitKeys(Resource):
    method_decorators = [authorize_decorator]

    def get(self):
        keys = hm.get_habit_keys()
        return keys
