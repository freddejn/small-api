from flask_restplus import Resource
from flask import jsonify, request
import datetime

class TimeApi(Resource):
    def get(self):
        """ Return the current time """
        auth = request.authorization
        if not auth:
            return ('Unauthorized', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'
            })
        print(auth)
        current_time = datetime.datetime.now().time()
        # user = datastore.Entity(datastore_client.key('User'))
        # user.update({'email':'test@email.com', 'password':'1234'})
        # datastore_client.put(user)
        return jsonify({'time': f'Current time is {current_time}'})
