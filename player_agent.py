class PlayerAgent:
    def __init__(self):
        pass

    def get_move(self, board):
        legal_arr = [str(move) for move in board.legal_moves]
        valid = False
        while not valid:
            move = input('Enter move: ')
            if move in legal_arr:
                return move
            print('Invalid. Try again.')