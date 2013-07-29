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
                square = self.board_state[y][x]
                if len(square) > 0:
                    if square[0]['type'] == 'snake_head':
                        if square[0]['id'] == self.client_id:
                            self.player_coords = (x, y)
                            print "PLAYER COORDS:", self.player_coords
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
            if obj['type'] == 'food':
                return self.STATE_FOOD
            if obj['type'] == 'snake':
                return self.STATE_BODY
            if obj['type'] == 'snake_head':
                return self.STATE_HEAD

        return self.STATE_EMPTY

    def is_empty(self, x, y):
        if self.is_wall(x, y):
            return False
        return self.get_state(x, y) == self.STATE_EMPTY

    def is_food(self, x, y):
        if self.is_wall(x, y):
            return False
        return self.get_state(x, y) == self.STATE_FOOD

    def is_snake(self, x, y):
        if self.is_wall(x, y):
            return False
        return (self.is_body(x, y)) or (self.is_head(x, y))

    def is_head(self, x, y):
         if self.is_wall(x, y):
            return False
        return (self.get_state(x, y) == self.STATE_HEAD)

    def is_body(self, x, y):
         if self.is_wall(x, y):
            return False
        return (self.get_state(x, y) == self.STATE_BODY)

    def is_wall(self, x, y):
        return x < 0 or x >= self.get_width() or y < 0 or y >= self.get_height()

    def allowed_moves(self):

        moves = ['n', 'e', 'w', 's']

        for item in self.items_in_range(self.player_coords[0], self.player_coords[1], search=1):
            if not self.is_food(item[0], item[1]):
                moves.remove(self.get_direction_to_point(item[0], item[1]))

        return moves

    def items_in_range(self, px, py, search=5):

        items = {}

        for y in range(self.get_height()):
            for x in range(self.get_width()):
                if self.calc_distance(px, py, x, y) <= search and self.is_empty(x,y):
                    items[(x,y)] = self.calc_distance(px, py, x, y)

        if items:
            return list(sorted(items, key=items.__getitem__))

        return []

    def calc_distance(self, x1, y1, x2, y2):
        return int(math.fabs(x1 - x2)) + int(math.fabs(y1 - y2))

    def get_distance_to_point(self, x, y):
        return self.calc_distance(self.player_coords[0], self.player_coords[1], x, y)

    def get_direction_to_point(self, x, y):
        self_x, self_y = self.player_coords

        d_x = int(math.fabs(self_x - x))
        d_y = int(math.fabs(self_y - y))

        if d_x > d_y:
            if self_x > x:
                return 'w'
            return 'e'

        if self_y > y:
            return 'n'
        return 's'
