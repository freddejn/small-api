from google.cloud import datastore
import datetime
import base64


class HabitModel():

    def store_habit(self, habit):
        client = datastore.Client()
        text = habit['body']
        habit_key = client.key('habit', str(
            base64.b64encode(text.encode('utf-8')), 'utf-8'))
        habit_entity = datastore.Entity(habit_key)
        habit_entity.update(habit)
        client.put(habit_entity)
        return {'id': habit_entity.key.to_legacy_urlsafe().decode('utf-8')}

    def get_habits(self, limit=20):
        habits_list = []
        client = datastore.Client()
        query = client.query(kind='habit')
        habits = query.fetch(limit=limit)
        for habit in habits:
            habit['id'] = habit.key.to_legacy_urlsafe().decode('utf-8')
            habits_list.append(habit)
        return habits_list

    def get_habit(self, id):
        client = datastore.Client()
        key = datastore.Key.from_legacy_urlsafe(id)
        habit = client.get(key)
        if habit:
            habit['id'] = habit.key.to_legacy_urlsafe().decode('utf-8')
            return habit
        return None

    def delete_habit(self, id):
        client = datastore.Client()
        key = datastore.Key.from_legacy_urlsafe(id)
        client.delete(key)
        return {'success': True}

    def get_habit_keys_only(self):
        client = datastore.Client()
        query = client.query(kind='habit')
        query.keys_only()
        res = query.fetch()
        return res

    def get_habit_keys(self):
        habits = self.get_habit_keys_only()
        return [ent.key.to_legacy_urlsafe().decode('utf-8') for ent in habits]

    def delete_all_habits(self):
        habits = self.get_habit_keys_only()
        habit_keys = [ent.key for ent in habits]
        client = datastore.Client()
        client.delete_multi(habit_keys)
        return {'success': True}

    def complete_habit(self, id):
        client = datastore.Client()
        date = datetime.date.today()
        parent_key = datastore.Key.from_legacy_urlsafe(id)
        key = client.key('completed_habit',
                         date.isoformat(), parent=parent_key)
        completed_habit = datastore.Entity(key)
        completed_habit['datetime'] = datetime.datetime.utcnow()
        res = client.put(completed_habit)
        return res
