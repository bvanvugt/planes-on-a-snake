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

    # Calculate risk of going in the direction of clusters of snakes

    # Calculate risk of going in the direction of long snakes

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
    max_dist = 4
    for d in range(1, max_dist + 1):
        # Start east
        xd = d
        yd = 0
        dir = 'e'
        risk_factor = max_dist + 1 # start at max + 1, go down to 1
        cur_x = our_x + xd
        cur_y = our_y + yd

        # Calculate risk with proximity to walls
        if board.is_wall(cur_x, cur_y):
            _max_risk(prox_risk, dir, prox_risk[dir] + risk_factor * 1)

        # Calculate risk with proximity to snake bodies, including own snake body
        if board.get_state(cur_x, cur_y) == STATE_BODY:
            _max_risk(prox_risk, dir, prox_risk[dir] + risk_factor * 2)

        # Calculate risk with proximity to snake heads
        if board.get_state(cur_x, cur_y) == STATE_HEAD:
            _max_risk(prox_risk, dir, prox_risk[dir] + risk_factor * 3)

        xd -= 1
        yd += 1

    _max_risk(risk, 'n', prox_risk['n'])
    _max_risk(risk, 'e', prox_risk['e'])
    _max_risk(risk, 's', prox_risk['s'])
    _max_risk(risk, 'w', prox_risk['w'])
