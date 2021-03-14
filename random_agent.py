import chess
import random


class RandomAgent:
    def __init__(self):
        pass

    def get_move(self, board):
        legal_arr = [move for move in board.legal_moves]
        move = str(random.choice(legal_arr))
        return move