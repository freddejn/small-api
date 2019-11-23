# [START gae_python37_app]
import datetime
from flask import Flask, jsonify
from flask_restplus import Api
from google.cloud import datastore
from routes import time_api
import settings
import secrets

# If no entrypiont in app.yaml this file will be run with app
def init_app_settings():
    secret = settings.get_jwt_secret()
    if (secret):
        app.config['SECRET'] = settings.get_jwt_secret()
    else:
        secret = settings.generate_jwt_secret()
        settings.store_secret_in_datastore(secret)
        app.config['SECRET'] = secret

app = Flask(__name__)
api = Api(app=app)
init_app_settings()

api.add_resource(time_api.TimeApi, '/api/time')

if __name__ == '__main__':
    # Only for local runs
    app.run(host='127.0.0.1', port=8080, debug=True)
    app.testing = True
# [END gae_python37_app]
