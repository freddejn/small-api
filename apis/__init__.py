from flask_restplus import Api
from apis.time_api import api as time_api
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
api = Api(blueprint, authorizations=authorizations, security='basicAuth')
api.add_namespace(time_api)
