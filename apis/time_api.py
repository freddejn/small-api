import datetime
from flask_restplus import Namespace, Resource, fields

from models.authorization import authorize_decorator

api = Namespace('time', description='Time related operations')

time_response = api.model('Time', {
    'time': fields.String,
})


@api.route('')
class TimeApi(Resource):
    method_decorators = [authorize_decorator]

    @api.marshal_with(time_response)
    def get(self):
        """ Return the current time """
        current_time = datetime.datetime.now().time()
        return {'time': f'Current time is {current_time}'}
