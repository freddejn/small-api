from datetime import datetime
from flask import jsonify
from flask_restplus import Namespace, Resource, fields
from google.cloud import datastore
from models.formatters import DatetimeFormatter as dtf

from models.authorization import authorize_decorator

api = Namespace('note', description='Note api')


note = api.model(name='note', model={
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
            json_note['created_date'] = datetime.now().isoformat()
        note.update(json_note)
        notes.append(note)
    client.put_multi(notes)


def get_notes():
    client = datastore.Client()
    query = client.query(kind='notes')
    query.order = ['created_date']
    notes = query.fetch(limit=20)
    return list(notes)


@api.route('')
class Note(Resource):
    method_decorators = [authorize_decorator]
    @api.expect([note], validate=False)
    @api.response(200, 'Success', [note])
    def post(self):
        notes = api.payload
        store_notes(notes)
        return notes

    @api.response(200, 'Success', [note])
    def get(self):
        notes = get_notes()
        return notes
