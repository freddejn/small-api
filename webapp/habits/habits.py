from models.authorization import authorize_decorator
import requests
from flask import Blueprint, render_template,\
    request, redirect, url_for, abort
from datetime import datetime, timedelta

blueprint = Blueprint('habits',
                      __name__,
                      template_folder='../templates'
                      )


def get_week(date):
    week = []
    if date is None:
        date = datetime.today()
    else:
        try:
            date = datetime.strptime(date, '%Y%m%d')
        except ValueError:
            return None
    start = date - timedelta(days=datetime.weekday(date))
    week.append(start)
    for day in range(1, 6):
        a_day = (start + timedelta(days=day)).strftime('%Y%m%d')
        week.append(a_day)
    end = (start + timedelta(days=6)).strftime('%Y%m%d')
    week.append(end)
    week[0] = start.strftime('%Y%m%d')
    return week


def get_habits(username, password):
    response = requests.get(request.url_root[:-1] +
                            url_for('api.habits_habit'),
                            auth=(username, password))
    return response.json()


def get_completed_habits(habit_id, username, password, start_date, end_date):
    response = requests.get(request.url_root[:-1] + url_for(
        'api.habits_complete_habits', habit_id=habit_id, start=start_date, end=end_date),
        auth=(username, password))
    return response.json()


@blueprint.route('', defaults={'date': None}, methods=['GET'])
@blueprint.route('/<string:date>', methods=['GET'])
@authorize_decorator
def habits_startpage(date):
    # data = {'page': 'startpage', 'url': request.path}
    week = get_week(date)
    if week is None:
        return render_template('404.html',
                               data={'error': f'The date format "{date}" is wrong, should be "yyymmdd".'})
    data = {'week': week}
    days = ['Mon', 'Tue', 'Wen', 'Thu', 'Fri', 'Sat', 'Sun']
    data['days'] = days
    habits = get_habits(
        request.authorization['username'],
        request.authorization['password'])
    for habit in habits:
        completed_habits = []
        completed_habits_temp = get_completed_habits(habit_id=habit['id'],
                                                     username=request.authorization['username'],
                                                     password=request.authorization['password'],
                                                     start_date=week[0],
                                                     end_date=week[6])
        j = 0
        for i in range(0, len(week)):
            if j >= len(completed_habits_temp):
                j = j - 1
            if len(completed_habits_temp) == 0:
                completed_habits.append({'id': None})
            elif int(week[i]) == int(completed_habits_temp[j]['id']):
                completed_habits.append(completed_habits_temp[j])
                j = j + 1
            else:
                completed_habits.append({'id': None})
        habit['completed'] = completed_habits
    data['habits'] = habits
    return render_template('habits/habits_base.html',
                           title='Habits', data=data)
