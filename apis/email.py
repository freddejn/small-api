from flask_restplus import Namespace, fields, Resource
from flask import current_app
import requests
# from mailjet_rest import Client as mail_client

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
        config = current_app.config
        email_data = api.payload
        requests.post(
            config['EMAIL_API_URL'],
            auth=('api', config['EMAIL_API_KEY']),
            data={'from': f'{config["FULL_EMAIL"]}',
                  'to': [f'{email_data["to"]}'],
                  'subject': f'{email_data["subject"]}',
                  'text': f'{email_data["text"]}'})
        return {'success': True}
