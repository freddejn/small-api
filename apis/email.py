from flask_restplus import Namespace, fields, Resource
from flask import current_app
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
        config = current_app.config
        print(api.payload)  # This is a dict

        email_api_url = config['EMAIL_API_URL']
        email_data = {
            'from': f'mailgun@{config["EMAIL_DOMAIN"]}',
            'to': ["freddejn@gmail.com"],
            'subject': 'Hello',
            'text': 'Testing some Mailgun awesomness!'}
        email_auth = ('api', config["EMAIL_API_KEY"])
        print(email_data['from'])
        print(email_api_url)
        res = requests.post(email_api_url, auth=email_auth, data=email_data)
        print(res)
        return {'success': True}
