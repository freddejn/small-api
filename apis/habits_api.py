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

# completed_habits = api.model(name='completed-habits', model={
#     'habit_key': fields.String('Habit key')
# })


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


@api.route('/<string:id>')
class OneHabit(Resource):
    method_decorators = [authorize_decorator]

    def get(self, id):
        print('running')
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


@api.route('/complete/<string:id>')
class CompleteHabit(Resource):
    method_decorators = [authorize_decorator]

    # @api.expect(completed_habits, validate=False)
    # @api.response(200, 'Success', habit)
    def post(self, id):
        res = hm.complete_habit(id)
        return res, 200
