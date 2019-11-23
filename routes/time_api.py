from flask_restplus import Resource

class TimeApi(Resource):
    def get(self):
        """ Return the current time """
        current_time = datetime.datetime.now().time()
        # user = datastore.Entity(datastore_client.key('User'))
        # user.update({'email':'test@email.com', 'password':'1234'})
        # datastore_client.put(user)
        return jsonify({'time': f'Current time is {current_time}'})
