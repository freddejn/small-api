# [START gae_python37_app]
from flask import Flask

from apis import blueprint

# If no entrypoint in app.yaml this file will be run with app
app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix='/api/1')

if __name__ == '__main__':
    # Only for local runs
    app.run(host='127.0.0.1', port=8080, debug=True)
    app.testing = True
# [END gae_python37_app]
