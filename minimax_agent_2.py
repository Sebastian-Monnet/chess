import chess
import copy
import random
import evaluation_2



class MinimaxAgent:
    def __init__(self, depth, is_alpha_beta=True, square_weighting=False, ratio=False):
        self.depth = depth
        self.is_alpha_beta = is_alpha_beta
        self.square_weighting = square_weighting
        self.ratio = ratio

    def get_move(self, board):
        turn = board.fen().split(' ')[1]
        move_arr = MinimaxAgent.get_legal_moves(board)
        random.shuffle(move_arr)
        best_val = -10000
        best_ind = 0
        for i in range(len(move_arr)):
            new_board = copy.deepcopy(board)
            new_board.push(move_arr[i])
            if self.is_alpha_beta:
                new_val = self.alpha_beta(new_board, turn, self.depth, -10000, 10000)
            else:
                new_val = self.minimax(new_board, turn, self.depth)
            if new_val > best_val:
                best_val = new_val
                best_ind = i
        return str(move_arr[best_ind])



    @staticmethod
    def get_legal_moves(board):
        legal_arr = [move for move in board.legal_moves]
        return legal_arr

    def alpha_beta(self, board, true_player, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            return evaluation_2.evaluate(board, true_player, self.square_weighting, self.ratio)

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

                new_val = self.alpha_beta(new_board, true_player, depth - 1, alpha, beta)
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
                new_val = self.alpha_beta(new_board, true_player, depth - 1, alpha, beta)

                eval = min(eval, new_val)

                beta = min(beta, new_val)

                if alpha >= beta:
                    break
            return eval



#board = chess.Board(fen='7k/5B2/8/8/8/4K3/8/p7 b - - 0 31')
#board = chess.Board(fen='3k4/3r4/8/8/8/3BK3/p7/8 w - - 0 30')
board = chess.Board(fen='7k/7p/7R/8/8/8/K7/8 w - - 0 30')

#print(board)
#print(MinimaxAgent.evaluate(board, 'w'))