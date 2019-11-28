from flask_restplus import Namespace, fields, Resource
from flask import current_app
from mailjet_rest import Client as mail_client
import requests

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
        # config = current_app.config
        print(api.payload)  # This is a dict
        # result = mailjet.send.create(data=email_data)
        # print(result.status_code)
        # print(result.json())
        return {'success': True}
