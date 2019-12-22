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
    method_decorators = [authorize_decorator]
    @api.response(200, 'Success', trivia)
    def post(self):
        trivia = store_trivia()
        return trivia


@api.route('/<int:id>')
@api.param('id', 'The game id')
class Trivia(Resource):
    method_decorators = [authorize_decorator]
    @api.response(200, 'Success', trivia)
    def get(self, id):
        print(id)
        return get_trivia(id)


@api.route('/<int:trivia_id>/player')
class TriviaJoin(Resource):
    method_decorators = [authorize_decorator]
    @api.expect(player_create)
    @api.response(200, 'Success')
    def post(self, trivia_id):
        player = api.payload
        result = join(trivia_id, player)
        return result
