from flask import request, make_response
from functools import wraps
from google.cloud import firestore
import google.cloud.exceptions


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
    db = firestore.Client()
    users = db.collection(u'users').document(u'{}'.format(username))
    try:
        user = users.get()
        return user.to_dict()
    except google.cloud.exceptions.NotFound:
        return None


def log_failed_attempt(request):
    db = firestore.Client()
    failedAttempt = {u'date_time': firestore.SERVER_TIMESTAMP,
                     u'authorization': str(request.authorization),
                     u'headers': str(request.headers),
                     u'remote_addr': str(request.remote_addr)
                     }
    db.collection(u'failedLogins').add(failedAttempt)
