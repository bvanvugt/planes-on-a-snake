import math


class Board():
    STATE_EMPTY = 'empty'
    STATE_FOOD = 'food'
    STATE_BODY = 'body'
    STATE_HEAD = 'head'

    def __init__(self, board_state, client_id):
        self.board_state = board_state
        self.client_id = client_id
        self.player_coords = None

        for y in range(self.get_height()):
            for x in range(self.get_width()):
                square = self.board[y][x]
                if len(square) > 0:
                    if square[0].type == 'snake_head' and square[0].id == client_id:
                        self.player_coords = (x, y)
                        return

        raise Exception('Board init fucked up')

    def get_head(self):
        return self.player_coords

    def get_id(self):
        self.client_id

    def get_width(self):
        return len(self.board_state[0])

    def get_height(self):
        return len(self.board_state)

    def get_state(self, x, y):
        """ snake|food|snake_head """
        square = self.board_state[y][x]

        if len(square) > 0:
            obj = square[0]
            if obj.type == 'food':
                return self.STATE_FOOD
            if obj.type == 'body':
                return self.STATE_BODY
            if obj.type == 'head':
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

