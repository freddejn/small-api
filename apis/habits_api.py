from flask_restplus import Namespace, Resource, fields
from models.habits import HabitModel, CompletedHabitModel

from models.authorization import authorize_decorator
hm = HabitModel()
chm = CompletedHabitModel()

api = Namespace('habits', description='Habit api')


habit = api.model(name='habit', model={
    'id': fields.String('Entity id'),
    'body': fields.String(description='The habit text.'),
    'keywords': fields.List(fields.String('Keyword')),
    'repetition': fields.Integer('Weekly repetition goal, e.g 1, 7')
})

completed_habit = api.model(name='completed_habit', model={
    'id': fields.Date(description='The date of completion'),
    'habit_id': fields.String(description='Id of corresponding habit.'),
    'timestamp': fields.DateTime(descripion='Datetime of update in database')
})

deleted = api.model(name='deleted', model={
    'timestamp': fields.DateTime(descripion='Datetime of update in database')
})


@api.route('')
class Habit(Resource):
    method_decorators = [authorize_decorator]
    @api.expect(habit, validate=False)
    @api.response(200, 'Success', habit)
    def post(self):
        habit = api.payload
        habit = hm.store_habit(habit)
        return habit

    @api.response(200, 'Success', [habit])
    def get(self):
        habits = hm.get_habits()
        return habits


@api.route('/<string:id>')
class OneHabit(Resource):
    method_decorators = [authorize_decorator]

    def get(self, id):
        habit = hm.get_habit(id)
        if habit is None:
            return {}, 404
        return habit, 200

    @api.response(200, 'Success', deleted)
    def delete(self, id):
        result = hm.delete_habit(id)
        return result


@api.route('/<string:habit_id>/completed', doc={'habit_id': 'The id of the corresponding habit.'})
class CompleteHabits(Resource):
    method_decorators = [authorize_decorator]

    @api.response(200, 'Success', completed_habit)
    def post(self, habit_id):
        completed_habit = chm.store_completed_habit(habit_id)
        if completed_habit is None:
            return {}, 404
        return completed_habit, 200

    @api.response(200, 'Success', completed_habit)
    def get(self, habit_id):
        completed = chm.get_completed_habits(habit_id)
        if not completed:
            return {}, 404
        return completed

    @api.response(200, 'Success', deleted)
    def delete(self, habit_id):
        res = chm.delete_completed_habits_by_habit_id(habit_id)
        return res


@api.route('/<string:habit_id>/completed/<string:date_completed>')
class CompletedHabit(Resource):

    @api.response(200, 'Success', completed_habit)
    def post(self, habit_id, date_completed=None):
        correct_date_format, error = chm.correct_date_format(date_completed)
        if not correct_date_format:
            return {'error': error}
        completed_habit = chm.store_completed_habit(habit_id, date_completed)
        if completed_habit is None:
            return {}, 404
        return completed_habit, 200
