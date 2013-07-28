def calc_risk(self, board):
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
    last_move = board.get_head().get_last_move()
    
    if last_move == 'e':
        risk['w'] = 99
    elif last_move == 'w':
        risk['e'] = 99
    elif last_move == 'n':
        risk['s'] = 99
    elif last_move == 's':
        risk['n'] = 99
        
    # Calculate risk with proximity to walls
    
    # Calculate risk with proxomity to snake bodies
    
    # Calculate risk with proximity to snake heads
    
    # Calculate risk of going in the direction of clusters of snakes
    
    # Calculate risk of going in the direction of long snakes
    
    return risk

# Pick the max of current risk and desired risk
def _max_risk(risk, direction, desired_risk):
    if risk[direction] < desired_risk:
        risk[direction] = desired_risk
