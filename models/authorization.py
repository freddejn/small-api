from flask import request, make_response
from functools import wraps
from google.cloud import datastore
import datetime

def authorize_decorator(func):
    @wraps(func)
    def authorize(*args, **kwargs):
        auth = request.authorization
        if not (auth and password_correct(auth.username, auth.password)):
            log_failed_attempt(request)
            return make_response('Unauthorized', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'
            })
        return func(*args, **kwargs)
    return authorize


def password_correct(username, password):
    if not username:
        return False
    user = get_user(username)
    if not user:
        return False
    stored_password = user['password']
    return (stored_password == password)


def get_user(username):
    client = datastore.Client()
    kind = 'User'
    key = client.key(kind, username)
    user = client.get(key)
    return user


def log_failed_attempt(request):
    client = datastore.Client()
    key = client.key('FailedLogin')
    log_entry = datastore.Entity(key)
    log_entry['datetime'] = datetime.datetime.now()
    log_entry['authorization'] = str(request.authorization)
    log_entry['headers'] = str(request.headers)
    log_entry['remote_addr'] = str(request.remote_addr)
    client.put(log_entry)
