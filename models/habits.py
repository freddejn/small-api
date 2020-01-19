from google.cloud import datastore
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
        return {'id': habit_entity.key.id}

    def get_habits(self, limit=20):
        habits_list = []
        client = datastore.Client()
        query = client.query(kind='habit')
        habits = query.fetch(limit=limit)
        for habit in habits:
            habit['id'] = habit.key.id_or_name
            habits_list.append(habit)
        return habits_list

    def get_habit(self, id):
        client = datastore.Client()
        key = client.key('habit', id)
        habit = client.get(key)
        habit['id'] = key.id
        return habit

    def delete_habit(self, id):
        client = datastore.Client()
        key = client.key('habit', id)
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
        return [ent.key.id_or_name for ent in habits]

    def delete_all_habits(self):
        habits = self.get_habit_keys_only()
        habit_keys = [ent.key for ent in habits]
        client = datastore.Client()
        client.delete_multi(habit_keys)
        return {'success': True}
