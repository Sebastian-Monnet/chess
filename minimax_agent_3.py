import chess
import copy
import random
import evaluation_2
import priorities


class MinimaxAgent:
    def __init__(self, depth, square_weighting=False, ratio=False):
        '''
        :param depth: depth of initial exploration
        :param is_alpha_beta:
        :param square_weighting:
        :param ratio:
        '''
        self.depth = depth
        self.square_weighting = square_weighting
        self.ratio = ratio

        self.move_dic = {}


    def get_move_values(self, move_arr, board, turn, depth):
        move_values = []
        for i in range(len(move_arr)):
            new_board = copy.deepcopy(board)
            new_board.push(move_arr[i])
            new_val = self.alpha_beta(new_board, turn, depth, -10000, 10000)

            move_values.append((move_arr[i], new_val))
        move_values = sorted(move_values, key=lambda tup: tup[1], reverse=True)
        return move_values

    def get_move(self, board):
        turn = board.fen().split(' ')[1]
        move_arr = MinimaxAgent.get_legal_moves(board)
        random.shuffle(move_arr)
        for i in range(self.depth + 1):
            move_values = self.get_move_values(move_arr, board, turn, self.depth)
            move_arr = [tup[0] for tup in move_values]




        return str(move_values[0][0])




    @staticmethod
    def get_legal_moves(board):
        legal_arr = [move for move in board.legal_moves]
        return legal_arr



    def alpha_beta(self, board, true_player, depth, alpha, beta):
        fen = board.fen()

        if depth == 0 or board.is_game_over():
            return evaluation_2.evaluate(board, true_player)

        to_play = board.fen().split(' ')[1]
        if to_play == true_player:
            is_maximise = True
        else:
            is_maximise = False

        if fen in self.move_dic:
            move_arr = self.move_dic[fen]
        else:
            move_arr = MinimaxAgent.get_legal_moves(board)
        move_val_arr = []

        if is_maximise:
            eval = -10000
            for move in move_arr:
                new_board = copy.deepcopy(board)
                new_board.push(move)

                new_val = self.alpha_beta(new_board, true_player, depth - 1, alpha, beta)
                alpha = max(alpha, new_val)
                '''print(new_board)
                print(new_board.fen())
                print('eval of ^:', new_val, 'depth:', depth-1)'''
                eval = max(eval, new_val)
                move_val_arr.append((move, new_val))
                if alpha >= beta:
                    break
                move_val_arr.append((move, new_val))
            move_val_arr = sorted(move_val_arr, key=lambda tup: tup[1], reverse=True)
            self.move_dic[fen] = [tup[0] for tup in move_val_arr]

            return eval

        else:
            eval = 10000
            for move in MinimaxAgent.get_legal_moves(board):
                new_board = copy.deepcopy(board)
                new_board.push(move)
                new_val = self.alpha_beta(new_board, true_player, depth - 1, alpha, beta)
                '''print(new_board)
                print(new_board.fen())
                print('eval of ^:', new_val, 'depth:', depth - 1)'''

                eval = min(eval, new_val)

                beta = min(beta, new_val)

                if alpha >= beta:
                    break
                move_val_arr.append((move, new_val))

            move_val_arr = sorted(move_val_arr, key=lambda tup: tup[1])
            self.move_dic[fen] = [tup[0] for tup in move_val_arr]
            return eval

'''a = MinimaxAgent(2)


board = chess.Board(fen='r1bqkbnr/pppppppp/2n5/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1')

print(a.alpha_beta(board, 'b', 2, -10000, 10000))

board = chess.Board(fen='r1bqkbnr/pppppppp/2n5/3P4/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 2')

print(a.alpha_beta(board, 'b', 1, -10000, 10000))'''

