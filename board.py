

class Board():
    STATE_EMTPY = 'empty'
    STATE_FOOD = 'food'
    STATE_BODY = 'body'
    STATE_HEAD = 'head'

    def __init__(self, board_state):
        self.board_state = board_state

    def get_width(self):
        return len(self.board_state[0])

    def get_height(self):
        return len(self.board_state)

    def get_state(self, x, y):
        """ snake|food|snake_head """
        square = self.board_state[y][x]

        if square.type == 'food':
            return self.STATE_FOOD
        if square.type == 'body':
            return self.STATE_BODY
        if square.type == 'head':
            return self.STATE_HEAD
        return self.STATE_EMTPY

    def is_empty(self, x, y):
        return self.get_state(x, y) == self.STATE_EMTPY

    def is_food(self, x, y):
        return self.get_state(x, y) == self.STATE_FOOD

    def is_snake(self, x, y):
        return (self.get_state(x, y) == self.STATE_BODY) or (self.get_state(x, y) == self.STATE_HEAD)


    def calc_distance(self, x1, y1, x2, y2):
        return int(math.fabs(x1 - x2)) + int(math.fabs(y1 - y2))
