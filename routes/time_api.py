from flask_restplus import Resource, Namespace
from flask import jsonify, request
import datetime
from models.authorization import authorize_decorator
api = Namespace('time', description='Time related operations')


@api.route('')
class TimeApi(Resource):
    method_decorators = [authorize_decorator]

    def get(self):
        """ Return the current time """
        current_time = datetime.datetime.now().time()
        return {'time': f'Current time is {current_time}'}
