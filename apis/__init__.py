from flask_restplus import Api
from apis.time_api import api as time_api
from apis.qr_code_api import api as qr_code_api
from apis.email import api as email_api
from apis.note_api import api as note_api
from flask import Blueprint

# api = Api(title='API for all sorts of things', version='1.0', endpoint='api')
authorizations = {
    'basicAuth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    }
}

blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0',
          endpoint='api', authorizations=authorizations, security='basicAuth')
api.add_namespace(time_api)
api.add_namespace(qr_code_api)
api.add_namespace(email_api)
api.add_namespace(note_api)
