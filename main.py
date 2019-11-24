# [START gae_python37_app]
import secrets

from flask import Flask
from flask_restplus import Api
from google.cloud import datastore

import config
from models.authorization import authorize_decorator
from routes import blueprint as api
from routes import time_api

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
init_app_settings()
app.register_blueprint(api, url_prefix='/api/1')

if __name__ == '__main__':
    # Only for local runs
    app.run(host='127.0.0.1', port=8080, debug=True)
    app.testing = True
# [END gae_python37_app]
