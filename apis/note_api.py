import datetime
from flask_restplus import Namespace, Resource, fields
from google.cloud import datastore

from models.authorization import authorize_decorator

api = Namespace('note', description='Note api')


note = api.model(name='note', model={
    'created_date': fields.DateTime(dt_format='iso8601'),
    'body': fields.String(description='The note body.'),
    'title': fields.String(description='The title of the note'),
    'keywords': fields.List(fields.String('Keyword')),
    'author': fields.String(description='The author of the note'),
})


def store_notes(json_notes):
    notes = []
    client = datastore.Client()
    json_notes = api.payload
    for json_note in json_notes:
        key = client.key('notes')
        note = datastore.Entity(key)
        if not json_note['created_date']:
            json_note['created_date'] = datetime.datetime.now().isoformat()
        note.update(json_note)
        notes.append(note)
    client.put_multi(notes)


def get_notes():
    notes_list = []
    client = datastore.Client()
    query = client.query(kind='notes')
    notes = query.fetch()
    for note in notes:
        notes_list.append(note)
    return notes_list


@api.route('')
class Note(Resource):
    method_decorators = [authorize_decorator]
    @api.expect([note], validate=False)
    @api.response(200, 'Success', [note])
    def post(self):
        notes = api.payload
        for note in notes:
            store_notes(note)
        print(notes)
        return notes

    @api.response(200, 'Success', [note])
    def get(self):
        return get_notes()
