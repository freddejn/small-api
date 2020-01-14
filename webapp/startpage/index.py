from flask import Blueprint, render_template, current_app, request
import os

# current_file_path = os.path.dirname(os.path.abspath(__file__))
blueprint = Blueprint('index',
                      __name__,
                      template_folder='../templates'
                      )


def this_path(app_context, request):
    api_endpoint = app_context.config['API_ENDPOINT']
    api_full_link = os.path.join(request.base_url, api_endpoint.lstrip('/'))
    return api_full_link


@blueprint.route('/index', methods=['GET'])
@blueprint.route('/', methods=['GET'])
def index():
    data = {
        'endpoint': current_app.config['API_ENDPOINT'],
        'full_endpoint': this_path(current_app, request)
    }
    print(data)
    return render_template('index.html', title='Home', data=data)
