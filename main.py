# [START gae_python37_app]
from flask import Flask
from instance.config import Config

from apis import blueprint as blueprint_api
from webapp.startpage.index import blueprint as blueprint_index

# If no entrypoint in app.yaml this file will be run with app
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(blueprint_api, url_prefix=app.config['API_ENDPOINT'])
app.register_blueprint(blueprint_index, url_prefix='/')

if __name__ == '__main__':
    # Only for local runs
    app.run(host='127.0.0.1', port=8080, debug=True)
    app.testing = True
# [END gae_python37_app]
