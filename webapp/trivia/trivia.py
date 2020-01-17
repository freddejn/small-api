from models.authorization import authorize_decorator
import requests
from flask import Blueprint, render_template,\
    request, redirect, url_for

blueprint = Blueprint('trivia',
                      __name__,
                      template_folder='../templates'
                      )


def get_trivia(trivia_id):
    response = requests.get(request.url_root[:-1] +
                            url_for('api.trivia_trivia', trivia_id=trivia_id))
    return response.json()


def create_trivia():
    response = requests.post(request.url_root[:-1] +
                             url_for('api.trivia_trivia_list'))
    return response.json()


def add_user_to_trivia(trivia_id, username):
    return requests.post(request.url_root[:-1] +
                         url_for('api.trivia_trivia_join',
                                 trivia_id=trivia_id),
                         json={'name': username})


@blueprint.route('', methods=['GET'])
def new_trivia():
    data = {'page': 'startpage', 'url': request.path}
    return render_template('trivia/trivia_base.html', title='Trivia', data=data)


@blueprint.route('/start', methods=['GET'])
@authorize_decorator
def start_trivia():
    trivia = create_trivia()
    return redirect(url_for('trivia.play_trivia', trivia_id=trivia['id']))


@blueprint.route('/<int:trivia_id>', methods=['GET'])
def play_trivia(trivia_id):
    trivia = get_trivia(trivia_id)
    data = {'page': 'gamepage', 'trivia_id': trivia_id}
    username = request.args.get('username')
    data['username'] = username
    data['trivia'] = trivia
    if not trivia:
        return redirect(url_for('trivia.new_trivia'))
    if not username:
        return redirect(url_for('trivia.create_user', trivia_id=trivia_id))
    return render_template('trivia/trivia_base.html', title='Trivia', data=data)


@blueprint.route('/create_user', methods=['GET'])
def create_user():
    data = {}
    username = request.args.get('username')
    data['trivia_id'] = request.args.get('trivia_id')
    data['page'] = 'create'
    if not username:
        return render_template('trivia/trivia_base.html', data=data)
    response = add_user_to_trivia(
        username=username,
        trivia_id=data['trivia_id'])
    if response.status_code == 200:
        return redirect(url_for('trivia.play_trivia',
                                trivia_id=data['trivia_id'],
                                username=username))
