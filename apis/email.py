from flask_restplus import Namespace, fields, Resource

from models.authorization import authorize_decorator

api = Namespace('email', description='Send email')

request_parser = api.model(name='Email', model={
    'to': fields.String(required=True, description='Whom to send the email to.'),
    'subject': fields.String(required=True, description='The subject field.'),
    'text': fields.String(required=True, description='The message text.'),
})


@api.route('')
class EmailApi(Resource):
    method_decorators = [authorize_decorator]

    @api.expect(request_parser, validate=True)
    def post(self):
        print(api.payload) # This is a dict
        return {'success': True}
