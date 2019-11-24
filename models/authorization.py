from flask import request, make_response
from functools import wraps


def check_auth(username, password):
    return (username == 'username' and password == 'password')


def authorize_decorator(func):
    @wraps(func)
    def authorize(*args, **kwargs):
        auth = request.authorization
        if not (auth and check_auth(auth.username, auth.password)):
            return make_response('Unauthorized', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'
            })
        return func(*args, **kwargs)
    return authorize
