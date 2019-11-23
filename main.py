# [START gae_python37_app]
import datetime
from flask import Flask
from google.cloud import datastore
import settings
import secrets

def init_app_settings():
    secret = settings.get_jwt_secret()
    if (secret):
        app.config['SECRET'] = settings.get_jwt_secret()
    else:
        secret = settings.generate_jwt_secret()
        settings.store_secret_in_datastore(secret)
        app.config['SECRET'] = secret

# datastore_client = datastore.Client()

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
init_app_settings()

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/api/time')
def get_current_time():
    """ Return the current time """
    current_time = datetime.datetime.now().time()
    # user = datastore.Entity(datastore_client.key('User'))
    # user.update({'email':'test@email.com', 'password':'1234'})
    # datastore_client.put(user)
    return f'Current time is {current_time}'

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
    app.testing = True
# [END gae_python37_app]
