# Required to make bottle work with gevent
import gevent.monkey
gevent.monkey.patch_all()

import bottle
import json
import os
import random


def _respond(response_json):
    return json.dumps(response_json)


@bottle.post('/<ai_mode>/register')
def register(ai_mode):
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- REGISTER ---", str(ai_mode)
    print "Game ID:", request.get('game_id')
    print "Client ID:", request.get('client_id')
    print "Board:"
    print "  Width:", request.get('board').get('width')
    print "  Height:", request.get('board').get('height')
    print "----------------"

    return _respond({
        'name': 'PlanesOnA Snake',
        'head_img_url': "http://fc02.deviantart.net/fs70/f/2010/148/3/d/20x20_PNG_Icons_sword_by_JMcIvor.png"
    })


@bottle.post('/<ai_mode>/start')
def start(ai_mode):
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- START ---", str(ai_mode)
    print "Game ID:", request.get('game_id')
    print "Num Players:", request.get('num_players')
    print "-------------"

    return _respond({})


@bottle.post('/<ai_mode>/tick/<client_id>')
def tick(ai_mode, client_id):
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- TICK", request.get('turn_num'), '---', str(ai_mode)
    print "Game ID:", request.get('id')
    print "Turn Num:", request.get('turn_num')
    print "Snakes:", len(request.get('snakes'))
    # print request.get('board')
    print "----------------"

    # Find the last move we made
    for snake in request.get('snakes'):
        if snake['id'] == client_id:
            my_snake = snake
            continue

    random_map = {
        'n': [random.choice(['n', 'e', 'w'])],
        's': [random.choice(['s', 'e', 'w'])],
        'w': [random.choice(['n', 's', 'w'])],
        'e': [random.choice(['n', 's', 'e'])],
        '': [random.choice(['n', 's', 'e', 'w'])]
    }

    # Map
    moves = random_map[my_snake['last_move']]
    my_move = moves[request.get('turn_num') % len(moves)]

    return _respond({
        'move': my_move,
        'message': 'Turn %d!' % (request.get('turn_num'))
    })


@bottle.post('<ai_mode>/end')
def end(ai_mode):
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- END ---", str(ai_mode)
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
