from models.authorization import authorize_decorator
import requests
from flask import Blueprint, render_template,\
    request, redirect, url_for

blueprint = Blueprint('habits',
                      __name__,
                      template_folder='../templates'
                      )


def get_habits(username, password):
    response = requests.get(request.url_root[:-1] +
                            url_for('api.habits_habit'),
                            auth=(username, password))
    return response.json()


@blueprint.route('', methods=['GET'])
@authorize_decorator
def habits_startpage():
    # data = {'page': 'startpage', 'url': request.path}
    data = {}
    habits = get_habits(
        request.authorization['username'], request.authorization['password'])
    data['habits'] = habits
    return render_template('habits/habits_base.html',
                           title='Habits', data=data)
