from flask_restplus import Namespace, Resource, fields
from google.cloud import datastore

from models.authorization import authorize_decorator

api = Namespace('habit', description='Habit api')


habit = api.model(name='habit', model={
    'body': fields.String(description='The habit text.'),
    'keywords': fields.List(fields.String('Keyword')),
    'repetition': fields.Integer('Weekly repetition goal, e.g 1, 7')
})


def store_habit(habit):
    client = datastore.Client()
    habit_key = client.key('habit')
    habit_entity = datastore.Entity(habit_key)
    habit_entity.update(habit)
    client.put(habit_entity)


def get_habits(limit=20):
    client = datastore.Client()
    query = client.query(kind='habit')
    habits = query.fetch(limit=limit)
    return list(habits)


@api.route('')
class Habit(Resource):
    method_decorators = [authorize_decorator]
    @api.expect(habit, validate=False)
    @api.response(200, 'Success', habit)
    def post(self):
        habit = api.payload
        store_habit(habit)
        return habit

    @api.response(200, 'Success', [habit])
    def get(self):
        habits = get_habits()
        return habits
