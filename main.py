# [START gae_python37_app]
# If no entrypoint in app.yaml this file will be run with app
from flask import Flask
from instance.config import Config

from apis import blueprint as blueprint_api
from apis import api as restplus_api
from webapp.startpage.index import blueprint as blueprint_webapp
from webapp.habits.habits import blueprint as blueprint_habits


app = Flask(__name__, static_url_path='/static', static_folder='webapp/static')
app.config.from_object(Config)
restplus_api.title = app.config['API_MANPAGE_TITLE']
app.register_blueprint(blueprint_api, url_prefix='/api/1')
app.register_blueprint(blueprint_webapp, url_prefix='')
app.register_blueprint(blueprint_habits, url_prefix='/habits')

if __name__ == '__main__':
    # Only for local runs
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
    app.testing = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['SERVER_NAME'] = 'http://localhost:8080'

# [END gae_python37_app]
