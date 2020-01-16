from flask_restplus import Namespace, Resource, fields
from google.cloud import datastore

from models.authorization import authorize_decorator

api = Namespace('trivia', description='Trivia api')


def store_trivia():
    client = datastore.Client()
    tkey = client.key('Trivia')
    key = client.allocate_ids(tkey, 1)[0]
    trivia = datastore.Entity(key)
    client.put(trivia)
    return {'id': key.id}


def get_trivia(key):
    client = datastore.Client()
    key = client.key('Trivia', key)
    entity = client.get(key)
    return entity


def name_taken(player, trivia):
    for other_player in trivia['players']:
        if other_player['name'] == player['name']:
            return True
    return False


def join(trivia_key, player):
    client = datastore.Client()
    key = client.key('Trivia', trivia_key)
    trivia = client.get(key)
    if trivia is None:
        return {}, 404
    if 'players' in trivia:
        if name_taken(player, trivia):
            return "Name already exists in game", 409
        trivia['players'].append(player)
    else:
        trivia['players'] = [player]
    client.put(trivia)
    return trivia


player_create = api.model(name='player_create', model={
    'name': fields.String('Player Name'),
})

trivia = api.model(name='trivia', model={
    'id': fields.String,
})


@api.route('')
class TriviaList(Resource):
    @api.response(200, 'Success', trivia)
    def post(self):
        trivia = store_trivia()
        return trivia


@api.route('/<int:trivia_id>')
@api.param('trivia_id', 'The game id')
class Trivia(Resource):
    @api.response(200, 'Success', trivia)
    def get(self, trivia_id):
        trivia = get_trivia(trivia_id)
        if trivia is not None:
            return {'id': trivia.id, 'players': trivia.get('players')}
        else:
            return {}, 404


@api.route('/<int:trivia_id>/player')
class TriviaJoin(Resource):
    @api.expect(player_create)
    @api.response(200, 'Success')
    def post(self, trivia_id):
        player = api.payload
        result = join(trivia_id, player)
        return result
