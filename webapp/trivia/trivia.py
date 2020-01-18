from models.authorization import authorize_decorator
import requests
import base64
from flask import Blueprint, render_template,\
    request, redirect, url_for, make_response

blueprint = Blueprint('trivia',
                      __name__,
                      template_folder='../templates'
                      )
current_question = {}


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
    return render_template('trivia/trivia_base.html',
                           title='Trivia', data=data)


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
    return render_template('trivia/trivia_base.html', title='Trivia',
                           data=data)


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


@blueprint.route('/new_question/<int:trivia_id>', methods=['GET'])
def new_question(trivia_id):
    response = requests.get('https://opentdb.com/api.php?amount=1')
    data = response.json()
    question = data['results'][0]['question']
    current_question[trivia_id] = {
        'hash': base64.b64encode(question.encode('utf-8')).decode('utf-8'),
        'question': data}
    return data


@blueprint.route('/get_updates/<int:trivia_id>', methods=['GET'])
def get_updates(trivia_id):
    question_hash = request.args.get('question')
    existing_question = current_question.get(trivia_id)
    if existing_question is None:
        return make_response({}, 304)
    if question_hash == existing_question.get('hash'):
        return make_response({}, 304)
    else:
        if existing_question.get('question'):
            return existing_question.get('question')
        return make_response({}, 304)
