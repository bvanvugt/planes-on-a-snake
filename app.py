# Required to make bottle work with gevent
import gevent.monkey
gevent.monkey.patch_all()

import bottle
import json
import os
import random

from board import Board
from reward import calc_reward
from risk import calc_risk


def _respond(response_json):
    return json.dumps(response_json)


@bottle.get('/')
def home():
    return "<h1>PLANES ON THE MUTHAFUCKING SNAKES</h1>"


@bottle.post('/register')
def register():
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- REGISTER ---"
    print "Game ID:", request.get('game_id')
    print "Client ID:", request.get('client_id')
    print "Board:"
    print "  Width:", request.get('board').get('width')
    print "  Height:", request.get('board').get('height')
    print "----------------"

    return _respond({
        'name': 'PlanesOnA Snake',
        'head_img_url': "http://bloatedcorpse.com/snakewithus/head-skull.gif",
        'tail_img_url': "http://bloatedcorpse.com/snakewithus/tail-skull.gif"
    })


@bottle.post('/start')
def start():
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- START ---"
    print "Game ID:", request.get('game_id')
    print "Num Players:", request.get('num_players')
    print "-------------"

    return _respond({})


@bottle.post('/tick/<client_id>')
def tick(client_id):
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- TICK", request.get('turn_num'), '---'
    print "Game ID:", request.get('id')
    print "Turn Num:", request.get('turn_num')
    print "Snakes:", len(request.get('snakes'))
    # print request.get('board')
    print "----------------"

    board = Board(request.get('board'), client_id)

    # Allowed moves
    (player_x, player_y) = board.get_head()
    allowed_moves = ['n', 's', 'e', 'w']

    def move_allowed(board, x, y):
        if x < 0 or x > (board.get_width() - 1):
            return False
        if y < 0 or y > (board.get_height() - 1):
            return False

        if board.is_snake(x, y):
            return False

        return True

    # East?
    if not move_allowed(board, (player_x - 1), player_y):
        allowed_moves.remove('e')
    # West?
    if not move_allowed(board, (player_x + 1), player_y):
        allowed_moves.remove('w')
    # South?
    if not move_allowed(board, player_x, (player_y + 1)):
        allowed_moves.remove('s')
    # North?
    if not move_allowed(board, player_x, (player_y - 1)):
        allowed_moves.remove('n')

    print "Allowed Moves:", allowed_moves

    # Calc Risk
    risk_scores = calc_risk(board)
    reward_scores = calc_reward(board)

    # Calc Reward
    calc_reward(board)

    return _respond({
        'move': 'n',
        'message': 'Turn %d!' % (request.get('turn_num'))
    })


@bottle.post('/end')
def end():
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- END ---"
    print "Game ID:", request.get('game_id')
    print "-------------"

    return _respond({})


## Runserver ##

prod_port = os.environ.get('PORT', None)

if prod_port:
    # Assume Heroku
    bottle.run(host='0.0.0.0', port=int(prod_port), server='gevent')
else:
    # Localhost
    bottle.debug(True)
    bottle.run(host='localhost', port=8080)
