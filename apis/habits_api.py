from flask_restplus import Namespace, Resource, fields
from flask import request
from models.habits import HabitModel, CompletedHabitModel

from models.authorization import authorize_decorator
hm = HabitModel()
chm = CompletedHabitModel()

api = Namespace('habits', description='Habit api')


habit = api.model('habit', {
    'body': fields.String('The habit text.'),
    'keywords': fields.List(fields.String('Keyword')),
    'repetition': fields.Integer('Weekly repetition goal, e.g 1, 7')
})

habit_response = api.inherit('habit_response', habit, {
    'id': fields.String('Habit id')
})

completed_habit = api.model('completed_habit', {
    'id': fields.Date(description='The date of completion'),
    'habit_id': fields.String('Id of corresponding habit.'),
    'timestamp': fields.DateTime('Datetime of update in database')
})

deleted = api.model('deleted', {
    'timestamp': fields.DateTime('Datetime of update in database')
})

updated = api.model('updated', {
    'timestamp': fields.DateTime('Datetime of update in database')
})


@api.route('')
class Habit(Resource):
    method_decorators = [authorize_decorator]
    @api.expect(habit, validate=False)
    @api.response(200, 'Success', habit_response)
    def post(self):
        habit = api.payload
        habit = hm.store_habit(habit)
        return habit

    @api.response(200, 'Success', [habit_response])
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

    @api.response(200, 'Success', updated)
    def post(self, id):
        result = hm.update_habit(id)
        return result

@api.route('/<string:habit_id>/completed',
           doc={'habit_id': 'The id of the corresponding habit.'})
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
        try:
            start_date = int(request.args.get('start'))
        except TypeError:
            start_date = None
        try:
            end_date = int(request.args.get('end'))
        except TypeError:
            end_date = None
        completed = chm.get_completed_habits(
            habit_id, start=start_date, end=end_date)
        if not completed:
            return {}, 404
        return completed

    @api.response(200, 'Success', deleted)
    def delete(self, habit_id):
        res = chm.delete_completed_habits_by_habit_id(habit_id)
        return res


@api.route('/<string:habit_id>/completed/<string:date_completed>')
class CompletedHabit(Resource):
    method_decorators = [authorize_decorator]

    @api.response(200, 'Success', completed_habit)
    def post(self, habit_id, date_completed=None):
        correct_date_format, error = chm.correct_date_format(date_completed)
        if not correct_date_format:
            return {'error': error}
        completed_habit = chm.store_completed_habit(habit_id, date_completed)
        if completed_habit is None:
            return {}, 404
        return completed_habit, 200

    @api.response(200, 'Success')
    def delete(self, habit_id, date_completed):
        correct_date_format, error = chm.correct_date_format(date_completed)
        if not correct_date_format:
            return {'error': error}
        deleted_habit = chm.delete_completed_habit(habit_id, date_completed)
        return deleted_habit
