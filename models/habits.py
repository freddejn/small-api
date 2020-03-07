from google.cloud import firestore
import google.cloud.exceptions
import datetime
from models.firestore_client import FirestoreClient


class Common(FirestoreClient):

    def correct_date_format(self, date_str):
        try:
            datetime.datetime.strptime(date_str, '%Y%m%d')
            return True, None
        except ValueError:
            return (False, f'Incorrect format of {date_str} should be YYYYmmdd')


class HabitModel(Common):

    def get_next(self, stream):
        obj = next(stream)
        if obj is None:
            return None
        return obj

    def store_habit(self, habit):
        if habit is None:
            return {}, 204
        db = firestore.Client()
        res = db.collection(u'habits').document()
        res.set(habit)
        habit['id'] = res.id
        return habit

    def get_habits(self, limit=20):
        habit_list = []
        db = firestore.Client()
        habits = db.collection(u'habits').stream()
        for habit in habits:
            habit_dict = habit.to_dict()
            habit_dict['id'] = habit.id
            habit_list.append(habit_dict)
        return habit_list

    def get_habit(self, id):
        db = firestore.Client()
        habit_ref = db.collection(u'habits').document(u'{}'.format(id))
        try:
            habit = habit_ref.get()
            habit_dict = habit.to_dict()
            habit_dict['id'] = habit.id
            return habit_dict
        except google.cloud.exceptions.NotFound:
            return None

    def delete_habit(self, id):
        db = firestore.Client()
        completed_habits_ref = db \
            .collection(u'habits') \
            .document(u'{}'.format(id)) \
            .collection(u'completed_habits')
        self.delete_all_documents(collection_ref=completed_habits_ref, data=[])
        habit_ref = db.collection(u'habits').document(id)
        res = habit_ref.delete()
        return {'deleted': res.ToJsonString(), 'id': id}

    def update_habit(self, data):
        db = firestore.Client()
        habit_ref = db.collection(u'habits').document(u'{}'.format(data['id']))
        habit_ref.set(data, merge=True)


class CompletedHabitModel(Common):
    def store_completed_habit(self, habit_id, date_completed=None):
        if date_completed is None:
            date_completed = datetime.date.today().strftime('%Y%m%d')
        db = firestore.Client()
        habits = db.collection('habits').document(u'{}'.format(habit_id)).get()
        if not habits.exists:
            return None
        completed_habit = {u'id': int(date_completed),
                           u'habit_id': habit_id,
                           u'timestamp': firestore.SERVER_TIMESTAMP}
        completed_habit_ref = db \
            .collection(u'habits') \
            .document(u'{}'.format(habit_id)) \
            .collection(u'completed_habits') \
            .document(u'{}'.format(date_completed))
        completed_habit_ref.set(completed_habit)
        completed_habit['timestamp'] = str(completed_habit['timestamp'])
        return completed_habit

    def get_completed_habits(self, habit_id, start=None, end=None):
        res = []
        db = firestore.Client()
        completed_habits_ref = db.collection(u'habits') \
            .document(u'{}'.format(habit_id)) \
            .collection(u'completed_habits')
        if start is None and end is None:
            completed_habits = completed_habits_ref.get()
        elif end is None:
            completed_habits = completed_habits_ref.where(
                u'id', u'>=', start).order_by(u'id').stream()
        elif start is None:
            completed_habits = completed_habits_ref.where(
                u'id', u'<=', end).order_by(u'id').stream()
        else:
            completed_habits = completed_habits_ref.where(
                u'id', u'<=', end).where(u'id', u'>=', start).order_by(u'id').stream()

        for completed_habit in completed_habits:
            tres = completed_habit.to_dict()
            tres['id'] = completed_habit.id
            tres['timestamp'] = str(tres['timestamp'])
            res.append(tres)
        return res

    def delete_completed_habits_by_habit_id(self, habit_id):
        db = firestore.Client()
        completed_habits_ref = db \
            .collection(u'habits') \
            .document(u'{}'.format(habit_id)) \
            .collection(u'completed_habits')
        res = self.delete_all_documents(completed_habits_ref, data=[])
        return res

    def delete_completed_habit(self, habit_id, completed_habit_id):
        db = firestore.Client()
        completed_habit = db \
            .collection(u'habits') \
            .document(u'{}'.format(habit_id)) \
            .collection(u'completed_habits').document(u'{}'.format(completed_habit_id))
        res = completed_habit.delete()

        return {'success': True,
                'habit_id': habit_id,
                'completed_date': completed_habit_id}
