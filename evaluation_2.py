import chess
import numpy as np


PIECE_VALUES = {'P' : 1, 'R' : 5, 'N' : 3.2, 'B' : 3.3, 'Q' : 9, 'K' : 900}
SQUARE_VALUE_WEIGHTING = 1

def get_square_value(i, j):
    UPPER_BOUND = 100
    return (UPPER_BOUND - max(abs(i - 3.5), abs(j - 3.5))) / (UPPER_BOUND - 0.5)

def evaluate(board, true_player, weights=(3, 200, 2, 0),print_vals=False):
    '''
    :param board: chess.Board() object
    :param true_player: player from whose perspective we compute the value
    :param weights:
    :param print_vals:
    :return:
    '''
    if board.is_game_over():
        result = board.result()
        if result == '1/2-1/2':
            return 0
        if result == '0-1':
            winner = 'b'
        elif result == '1-0':
            winner = 'w'
        if winner == true_player:
            return 100000
        else:
            return -100000

    mat_diff, mat_ratio = material_scores(board, true_player)
    dev = dev_score(board, true_player)
    central = central_squares(board, true_player)
    if print_vals:
        print('mat_diff, log ratio, central, total:', 3 * mat_diff, 200 * np.log(mat_ratio), 2*central, 3* mat_diff + 200 * np.log(mat_ratio) + central)

    #return 5 * mat_diff + 5 * np.log(mat_ratio) + 3 * dev + central
    return 3 * mat_diff + 200 * np.log(mat_ratio) + 2*central

def material_scores(board, true_player):
    row_arr = board.fen().split('/')
    row_arr[-1] = row_arr[-1].split(' ')[0]
    # value from white's perspective
    w_pts = 0
    b_pts = 0
    for i, row in enumerate(row_arr):
        j = 0
        for char in row:
            if not char.isalpha():
                j += int(char)
                continue
            abs_val = PIECE_VALUES[char.upper()]
            if char.isupper():
                w_pts += abs_val
            else:
                b_pts += abs_val
            j += 1
    if true_player == 'w':
        return w_pts - b_pts, w_pts/b_pts
    else:
        return b_pts - w_pts, b_pts/w_pts

def get_square_value(i, j):
    UPPER_BOUND = 5
    return (UPPER_BOUND - max(abs(i - 3.5), abs(j - 3.5))) / (UPPER_BOUND - 0.5)

def central_squares(board, true_player):
    w_pts = 0
    b_pts = 0
    row_arr = board.fen().split(' ')[0].split('/')
    for i, row in enumerate(row_arr):
        j = 0
        for char in row:
            if char.upper() == 'K':
                j += 1
                continue
            if not char.isalpha():
                j += int(char)
                continue
            abs_val = get_square_value(i, j)
            if char.isupper():
                w_pts += abs_val
            else:
                b_pts += abs_val
            j += 1
    #print(w_pts, b_pts)
    if true_player == 'w':
        return w_pts - b_pts
    else:
        return b_pts - w_pts
def num_central_pawns_in_row(rowstr):
    i = 0
    white, black = 0, 0
    for char in rowstr:
        if not char.isalpha():
            i += int(char)
            continue
        else:
            i+=1
        if char == 'p' and 3 <= i <= 4:
            black += 1
        elif char == 'P' and 3 <= i <= 4:
            white += 1
    return white, black

def dev_score(board, true_player):
    white, black = 4, 4
    rows = board.fen().split('/')
    rows[-1] = rows[-1].split(' ')[0]
    for char in rows[0]:
        if char == 'n' or char == 'b':
            black -= 1
    for char in rows[7]:
        if char == 'N' or char == 'B':
            white -= 1
    for i in range(3, 7):
        white_pawns, black_pawns = num_central_pawns_in_row(rows[i])
        white += white_pawns
        black += black_pawns
    if true_player == 'w':
        return white - black
    else:
        return black - white




board = chess.Board(fen='r2qkb1r/ppp1pppp/2n2n2/3p4/3P1Bb1/2N2N2/PPP1PPPP/R2QKB1R w KQkq - 0 1')
print(central_squares(board, 'b'))
