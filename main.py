# [START gae_python37_app]
import secrets
import config
from flask import Flask
from flask_restplus import Api
from google.cloud import datastore
from routes import time_api
from models.authorization import authorize_decorator

# If no entrypoint in app.yaml this file will be run with app


def init_app_settings():
    secret = config.get_jwt_secret()
    if (secret):
        app.config['SECRET'] = config.get_jwt_secret()
    else:
        secret = config.generate_jwt_secret()
        config.store_secret_in_datastore(secret)
        app.config['SECRET'] = secret


app = Flask(__name__)

authorizations = {
    'basicAuth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(app=app, authorizations=authorizations,
          security='Basic Auth', decorators=[authorize_decorator])
init_app_settings()

api.add_resource(time_api.TimeApi, '/api/time')

if __name__ == '__main__':
    # Only for local runs
    app.run(host='127.0.0.1', port=8080, debug=True)
    app.testing = True
# [END gae_python37_app]
