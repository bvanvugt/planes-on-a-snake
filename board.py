

class Board():
    PIECE_FOOD = 'food'
    PIECE_SNAKE_BODY = 'body'
    PIECE_SNAKE_HEAD = 'head'

    def __init__(self, board_state):
        self.board_state = board_state

    def get_width(self):
        return len(self.board_state[0])

    def get_height(self):
        return len(self.board_state)
