from flask import Blueprint, render_template, current_app, request
import os

# current_file_path = os.path.dirname(os.path.abspath(__file__))
blueprint = Blueprint('index',
                      __name__,
                      static_url_path='/',
                      static_folder='../static',
                      template_folder='../templates')


@blueprint.route('/index', methods=['GET'])
@blueprint.route('/', methods=['GET'])
def index():
    api_endpoint = current_app.config['API_ENDPOINT']
    api_full_link = os.path.join(request.base_url, api_endpoint.lstrip('/'))
    data = {
        'endpoint': current_app.config['API_ENDPOINT'],
        'full_endpoint': api_full_link
    }
    return render_template('index.html', title='Home', data=data)

@blueprint.route('/trivia', methods=['GET'])
def trivia():
    return render_template('trivia.html', title='Trivia')