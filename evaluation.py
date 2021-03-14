import chess

PIECE_VALUES = {'P' : 1, 'R' : 5, 'N' : 3.2, 'B' : 3.3, 'Q' : 9, 'K' : 900}
SQUARE_VALUE_WEIGHTING = 1

def get_square_value(i, j):
    UPPER_BOUND = 100
    return (UPPER_BOUND - max(abs(i - 3.5), abs(j - 3.5))) / (UPPER_BOUND - 0.5)

def evaluate(board, true_player, square_weighting=False, ratio=False, print_scores=False):
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
    w_pts = 0
    b_pts = 0
    for i, row in enumerate(row_arr):
        j = 0
        for char in row:
            if not char.isalpha():
                j += int(char)
                continue
            abs_val = PIECE_VALUES[char.upper()]
            if square_weighting and char.upper() != 'K':
                abs_val += get_square_value(i, j)
            if char.isupper():
                w_pts += abs_val
            else:
                b_pts += abs_val
            j += 1
    if ratio:
        val = w_pts / b_pts

    if print_scores:
        print('old_val:', w_pts, b_pts)
    if true_player == 'w' and ratio:
        return w_pts / b_pts
    elif true_player == 'w':
        return w_pts - b_pts
    elif true_player == 'b' and ratio:
        return b_pts / w_pts
    else:
        return b_pts - w_pts

'''board = chess.Board(fen='rnb1kbnr/1ppp1pp1/8/p3p1qp/2PP4/N6N/PP2PPPP/1R1QKB1R w Kkq - 0 7')
print(evaluate(board, 'w', square_weighting=True))

board = chess.Board(fen='rnb1kbnr/1ppp1pp1/8/p3p1Np/2PP4/N7/PP2PPPP/1R1QKB1R b Kkq - 0 7')
print(evaluate(board, 'w', square_weighting=True))

board = chess.Board(fen='rnb1kbnr/1ppp1pp1/8/p3p1qp/2PP4/NP5N/P3PPPP/1R1QKB1R b Kkq - 0 7')
print(evaluate(board, 'w', square_weighting=True))'''