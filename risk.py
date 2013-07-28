import math

from board import Board

def calc_risk(board, last_move):
    risk = {'n': 0,
            'e': 0,
            's': 0,
            'w': 0}

    our_x = board.get_head()[0]
    our_y = board.get_head()[1]

    # Easy risk calculation for bad moves
    # Don't hit walls
    if our_y == 0:
        risk['n'] = 100
    elif our_y == board.get_height():
        risk['s'] = 100

    if our_x == 0:
        risk['w'] = 100
    elif our_x == board.get_width():
        risk['e'] = 100

    # Don't hit other snakes (doesn't matter if self for now)
    if board.is_snake(our_x, our_y - 1):
        risk['n'] = 100
    if board.is_snake(our_x + 1, our_y):
        risk['e'] = 100
    if board.is_snake(our_x, our_y + 1):
        risk['s'] = 100
    if board.is_snake(our_x - 1, our_y):
        risk['w'] = 100

    # Don't hit self, but do it as a last resort
    if len(last_move) > 0:
        if last_move == 'e':
            risk['w'] = 99
        elif last_move == 'w':
            risk['e'] = 99
        elif last_move == 'n':
            risk['s'] = 99
        elif last_move == 's':
            risk['n'] = 99

    # Calculate proximity based risk
    _proximity_risk(board, risk, our_x, our_y)
    
    # Calculate risk of going in the direction of other snakes, considering snake length
    
    return risk

# Pick the max of current risk and desired risk
def _max_risk(risk, direction, desired_risk):
    max_risk = 98 # stay under suicide risk
    if risk[direction] < desired_risk:
        if desired_risk > max_risk:
            risk[direction] = 98
        else:
            risk[direction] = desired_risk

# Calculate proxomity risk
def _proximity_risk(board, risk, our_x, our_y):
    prox_risk = {'n': 0,
                 'e': 0,
                 's': 0,
                 'w': 0}
    max_dist = 4 # max proximity risk
    for d in range(1, max_dist + 1):
        # Start east
        xd = d
        yd = 0
        risk_factor = max_dist - d + 1
        cur_x = our_x + xd
        cur_y = our_y + yd

        # Circle south
        for i in range(d):
            xd -= 1
            yd += 1

            if abs(xd) > abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'e', risk_factor)
            elif abs(xd) < abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 's', risk_factor)
            elif abs(xd) == abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'e', risk_factor / 2.0)
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 's', risk_factor / 2.0)

        # Circle west
        for i in range(d):
            xd -= 1
            yd -= 1

            if abs(xd) > abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'w', risk_factor)
            elif abs(xd) < abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 's', risk_factor)
            elif abs(xd) == abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'w', risk_factor / 2.0)
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 's', risk_factor / 2.0)

        # Circle north
        for i in range(d):
            xd += 1
            yd -= 1

            if abs(xd) > abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'w', risk_factor)
            elif abs(xd) < abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'n', risk_factor)
            elif abs(xd) == abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'w', risk_factor / 2.0)
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'n', risk_factor / 2.0)

        # Circle east
        for i in range(d):
            xd += 1
            yd += 1

            if abs(xd) > abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'e', risk_factor)
            elif abs(xd) < abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'n', risk_factor)
            elif abs(xd) == abs(yd):
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'e', risk_factor / 2.0)
                _calc_prox_risk(board, cur_x, cur_y, prox_risk, 'n', risk_factor / 2.0)

    _max_risk(risk, 'n', prox_risk['n'])
    _max_risk(risk, 'e', prox_risk['e'])
    _max_risk(risk, 's', prox_risk['s'])
    _max_risk(risk, 'w', prox_risk['w'])

def _calc_prox_risk(board, cur_x, cur_y, prox_risk, dir, risk_factor):
    # Calculate risk with proximity to walls
    if board.is_wall(cur_x, cur_y):
        _max_risk(prox_risk, dir, prox_risk[dir] + ceil(risk_factor * 1))

    # Calculate risk with proximity to snake bodies, including own snake body
    if board.get_state(cur_x, cur_y) == Board.STATE_BODY:
        _max_risk(prox_risk, dir, prox_risk[dir] + ceil(risk_factor * 2))

    # Calculate risk with proximity to snake heads
    if board.get_state(cur_x, cur_y) == Board.STATE_HEAD:
        _max_risk(prox_risk, dir, prox_risk[dir] + ceil(risk_factor * 3))

def _get_snake_square_count(board, our_x, our_y):
    snake_count = {'n': (0, 0), # (heads, bodies)
                   'e': (0, 0),
                   's': (0, 0),
                   'w': (0, 0)}
    
    for x in range(board.get_width()):
        for y in range(board.get_height()):
            xd = x - our_x
            yd = y - our_y
            
            if xd == 0 and yd == 0:
                continue
            
            xdir = 'e'
            if xd < 0:
                xdir = 'w'
            ydir = 's'
            if xd < 0:
                ydir = 'n'

            if int(math.fabs(xd)) == int(math.fabs(yd)):
                if board.get_state(x, y) == Board.STATE_HEAD:
                    snake_count[xdir][0] += 0.5
                    snake_count[ydir][0] += 0.5
                elif board.get_state(x, y) == Board.STATE_BODY:
                    snake_count[xdir][1] += 0.5
                    snake_count[xdir][1] += 0.5
            elif int(math.fabs(xd)) > int(math.fabs(yd)):
                if board.get_state(x, y) == Board.STATE_HEAD:
                    snake_count[xdir][0] += 1
                elif board.get_state(x, y) == Board.STATE_BODY:
                    snake_count[xdir][1] += 1
            else: # north/south direction
                if board.get_state(x, y) == Board.STATE_HEAD:
                    snake_count[ydir][0] += 1
                elif board.get_state(x, y) == Board.STATE_BODY:
                    snake_count[ydir][1] += 1

def _calc_snake_risk(board, risk, our_x, our_y):
    snake_count = _get_snake_square_count(board, our_x, our_y)
    
    for dir in ['n', 'e', 's', 'w']:
        _max_risk(risk, dir, risk[dir] + math.ceil(snake_count[dir][0] * 2 + snake_count[dir][1] * 1))