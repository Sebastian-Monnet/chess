import chess
import copy
import random
import datetime

PIECE_VALUES = {'P' : 1, 'R' : 5, 'N' : 3.2, 'B' : 3.3, 'Q' : 9, 'K' : 900}

class MinimaxAgentIter:
    def __init__(self, depth):
        self.depth = depth

    def get_move(self, board, turn):
        move_arr = MinimaxAgentIter.minimax_iteration(board, self.depth)
        return str(random.choice(move_arr))

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
    def get_next_states(board, moves):
        true_fen = board.fen()
        state_arr = []
        for move in moves:
            board.set_fen(true_fen)
            board.push(move)
            state_arr.append(board.fen())
        return state_arr

    @staticmethod
    def minimax_iteration(board, max_depth):
        child_dic, parent_dic, val_dic, moves_dic = {}, {}, {}, {}

        cur_board = copy.deepcopy(board)

        cur_depth = 0
        root = board.fen()
        cur_node = root
        true_player = cur_node.split(' ')[1]
        add_children = True

        num_iters = 0
        d = datetime.datetime.now()
        while root not in val_dic:

            most_recent_lag = (datetime.datetime.now() - d).total_seconds()
            d = datetime.datetime.now()
            num_iters += 1
            if cur_depth == max_depth:
                val_dic[cur_node] = MinimaxAgentIter.evaluate(cur_board, true_player)
                cur_depth -= 1
                add_children = False
                if max_depth != 0:
                    cur_node = parent_dic[cur_node]
                    cur_board = chess.Board(cur_node)
                most_recent_lag = (datetime.datetime.now() - d).total_seconds()
                continue

            if add_children:
                moves = MinimaxAgentIter.get_legal_moves(cur_board)
                child_arr = MinimaxAgentIter.get_next_states(cur_board,moves)
                child_dic[cur_node] = child_arr
                for child in child_arr:
                    parent_dic[child] = cur_node
                add_children = False
                most_recent_lag = (datetime.datetime.now() - d).total_seconds()

            has_all_children = True
            for child in child_dic[cur_node]:
                if child not in val_dic:
                    cur_node = child
                    cur_board = chess.Board(cur_node)
                    cur_depth += 1
                    if child not in child_dic:
                        add_children = True
                    has_all_children = False
                    break
            most_recent_lag = (datetime.datetime.now() - d).total_seconds()

            if has_all_children:
                child_values = [val_dic[child] for child in child_dic[cur_node]]
                if child_values == []:
                    val_dic[cur_node] = MinimaxAgentIter.evaluate(cur_board, true_player)
                elif cur_depth % 2 == 0:
                    val_dic[cur_node] = max(child_values)
                else:
                    val_dic[cur_node] = min(child_values)
                if cur_depth > 0:
                    cur_node = parent_dic[cur_node]
                    cur_depth -= 1
                cur_board.set_fen(cur_node)
                most_recent_lag = (datetime.datetime.now() - d).total_seconds()

        b = datetime.datetime.now()

        moves = MinimaxAgentIter.get_legal_moves(board)
        best_move_arr = []
        best_val = -999999
        for move in moves:
            cur_board = chess.Board(cur_node)
            cur_board.push(move)
            if val_dic[cur_board.fen()] == best_val:
                best_move_arr.append(move)
            elif val_dic[cur_board.fen()] > best_val:
                best_val = val_dic[cur_board.fen()]
                best_move_arr = [move]
        c = datetime.datetime.now()


        return best_move_arr


class MinimaxAgentRecur:
    def __init__(self, depth):
        self.depth = depth

    def get_move(self, board, turn):
        move_arr = MinimaxAgentRecur.get_legal_moves(board)
        random.shuffle(move_arr)
        best_val = -10000
        best_ind = 0
        for i in range(len(move_arr)):
            new_board = copy.deepcopy(board)
            new_board.push(move_arr[i])
            new_val = MinimaxAgentRecur.minimax(new_board, turn, self.depth)
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
    def minimax(board, true_player, depth):
        if depth == 0 or board.is_game_over():
            return MinimaxAgentRecur.evaluate(board, true_player)

        to_play = board.fen().split(' ')[1]
        if to_play == true_player:
            is_maximise = True
        else:
            is_maximise = False

        if is_maximise:
            eval = -10000
            for move in MinimaxAgentRecur.get_legal_moves(board):
                new_board = copy.deepcopy(board)
                new_board.push(move)

                new_val = MinimaxAgentRecur.minimax(new_board, true_player, depth - 1)
                eval = max(eval, new_val)

            return eval

        else:
            eval = 10000
            for move in MinimaxAgentRecur.get_legal_moves(board):
                new_board = copy.deepcopy(board)
                new_board.push(move)
                new_val = MinimaxAgentRecur.minimax(new_board, true_player, depth - 1)

                eval = min(eval, new_val)
            return eval




#board = chess.Board(fen='7k/5B2/8/8/8/4K3/8/p7 b - - 0 31')
#board = chess.Board(fen='6k1/5r2/8/8/8/3BK3/p7/8 w - - 0 30')

#print(board)
#print(MinimaxAgentIter.minimax(board, 'w', 4))
#print(MinimaxAgentIter.evaluate(board, 'w'))
