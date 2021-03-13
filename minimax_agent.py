import chess
import copy
import random

PIECE_VALUES = {'P' : 1, 'R' : 5, 'N' : 3.2, 'B' : 3.3, 'Q' : 9, 'K' : 900}

class MinimaxAgent:
    def __init__(self, depth, is_alpha_beta=True):
        self.depth = depth
        self.is_alpha_beta = is_alpha_beta

    def get_move(self, board, turn):
        move_arr = MinimaxAgent.get_legal_moves(board)
        random.shuffle(move_arr)
        best_val = -10000
        best_ind = 0
        for i in range(len(move_arr)):
            new_board = copy.deepcopy(board)
            new_board.push(move_arr[i])
            if self.is_alpha_beta:
                new_val = MinimaxAgent.alpha_beta(new_board, turn, self.depth, -10000, 10000)
            else:
                new_val = MinimaxAgent.minimax(new_board, turn, self.depth)
            if new_val > best_val:
                best_val = new_val
                best_ind = i
        return str(move_arr[best_ind])


    @staticmethod
    def evaluate(board, true_player):
        if board.is_game_over():
            result = board.result()
            if result == '1/2-1/2':
                return 0
            if result == '0-1':
                winner = 'b'
            elif result == '1-0':
                winner = 'w'
            if winner == true_player:
                return 10000
            else:
                return -10000

        row_arr = board.fen().split('/')
        row_arr[-1] = row_arr[-1].split(' ')[0]

        # value from white's perspective
        val = 0
        for row in row_arr:
            for char in row:
                if not char.isalpha():
                    continue
                abs_val = PIECE_VALUES[char.upper()]
                if char.isupper():
                    val += abs_val
                else:
                    val -= abs_val

        if true_player == 'w':
            return val
        else:
            return - val
    @staticmethod
    def get_legal_moves(board):
        legal_arr = [move for move in board.legal_moves]
        return legal_arr

    @staticmethod
    def alpha_beta(board, true_player, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            return MinimaxAgent.evaluate(board, true_player)

        to_play = board.fen().split(' ')[1]
        if to_play == true_player:
            is_maximise = True
        else:
            is_maximise = False

        if is_maximise:
            eval = -10000
            for move in MinimaxAgent.get_legal_moves(board):
                new_board = copy.deepcopy(board)
                new_board.push(move)

                new_val = MinimaxAgent.alpha_beta(new_board, true_player, depth - 1, alpha, beta)
                alpha = max(alpha, new_val)
                #print(new_board)
                #print(new_board.fen())
                #print('eval of ^:', new_val, 'depth:', depth-1)
                eval = max(eval, new_val)
                if alpha >= beta:
                    break



            return eval

        else:
            eval = 10000
            for move in MinimaxAgent.get_legal_moves(board):
                new_board = copy.deepcopy(board)
                new_board.push(move)
                new_val = MinimaxAgent.alpha_beta(new_board, true_player, depth - 1, alpha, beta)

                eval = min(eval, new_val)

                beta = min(beta, new_val)

                if alpha >= beta:
                    break
            return eval

    @staticmethod
    def minimax(board, true_player, depth):
        if depth == 0 or board.is_game_over():
            return MinimaxAgent.evaluate(board, true_player)

        to_play = board.fen().split(' ')[1]
        if to_play == true_player:
            is_maximise = True
        else:
            is_maximise = False

        if is_maximise:
            eval = -10000
            for move in MinimaxAgent.get_legal_moves(board):
                new_board = copy.deepcopy(board)
                new_board.push(move)

                new_val = MinimaxAgent.minimax(new_board, true_player, depth - 1)
                eval = max(eval, new_val)

            return eval

        else:
            eval = 10000
            for move in MinimaxAgent.get_legal_moves(board):
                new_board = copy.deepcopy(board)
                new_board.push(move)
                new_val = MinimaxAgent.minimax(new_board, true_player, depth - 1)

                eval = min(eval, new_val)
            return eval


#board = chess.Board(fen='7k/5B2/8/8/8/4K3/8/p7 b - - 0 31')
#board = chess.Board(fen='3k4/3r4/8/8/8/3BK3/p7/8 w - - 0 30')
board = chess.Board(fen='7k/7p/7R/8/8/8/K7/8 w - - 0 30')

#print(board)
#print(MinimaxAgent.evaluate(board, 'w'))