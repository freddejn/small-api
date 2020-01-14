from models.authorization import authorize_decorator
import requests
from flask import Blueprint, render_template,\
    request, redirect, url_for

# current_file_path = os.path.dirname(os.path.abspath(__file__))
blueprint = Blueprint('trivia',
                      __name__,
                      template_folder='../templates'
                      )


@blueprint.route('', methods=['GET'])
def new_trivia():
    data = {'startpage': True, 'url': request.path}
    return render_template('trivia.html', title='Trivia', data=data)


@blueprint.route('/start', methods=['GET'])
@authorize_decorator
def start_trivia():
    data = {'startpage': False}
    response = requests.post(request.url_root[:-1] +
                             url_for('api.trivia_trivia_list'),
                             auth=(request.authorization['username'],
                                   request.authorization['password']))
    data = response.json()
    return redirect(url_for('trivia.play_trivia', trivia_id=data['id']))


@blueprint.route('/<int:trivia_id>', methods=['GET'])
@authorize_decorator
def play_trivia(trivia_id):
    # print(url_for('api.trivia_trivia', trivia_id=trivia_id)) # Importand TODO TODO TODO
    response = requests.get(request.url_root[:-1] +
                            url_for('api.trivia_trivia', trivia_id=trivia_id),
                            auth=(request.authorization['username'],
                                  request.authorization['password']))
                                  
    if not response.json():
        return redirect(url_for('trivia.new_trivia'))

    data = {'startpage': False, 'trivia_id': trivia_id}
    username = request.args.get('username')
    if username:
        return render_template('trivia.html', title='Trivia', data=data)
    return redirect(url_for('trivia.create_user', trivia_id=trivia_id))


@blueprint.route('/create_user', methods=['GET'])
def create_user():
    data = {}
    data['trivia_id'] = request.args.get('trivia_id')
    return render_template('create_user.html', data=data)
