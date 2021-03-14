import chess

PIECE_VALUES = {'P' : 1, 'R' : 5, 'N' : 3.2, 'B' : 3.3, 'Q' : 9, 'K' : 900}
SQUARE_VALUE_WEIGHTING = 1

def get_square_value(i, j):
    UPPER_BOUND = 100
    return (UPPER_BOUND - max(abs(i - 3.5), abs(j - 3.5))) / (UPPER_BOUND - 0.5)

def evaluate(board, true_player, square_weighting=False, ratio=False):
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

    return 5 * material_diff(board, true_player) + dev_score(board, true_player) + central_squares(board, true_player)

def material_diff(board, true_player):
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
        return w_pts - b_pts
    else:
        return b_pts - w_pts

def central_squares(board, true_player):
    centre = [chess.D4, chess.E4, chess.D5, chess.E5]
    white, black = 0, 0
    for square in centre:
        white += len(board.attackers(chess.WHITE, square))
        black += len(board.attackers(chess.BLACK, square))
    if true_player == 'w':
        return white - black
    else:
        return black - white
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



'''board = chess.Board(fen="r2qk2r/ppp2ppp/2n2n2/2PpB3/6b1/2N2N1P/PPP1PPP1/R2QKB1R b KQkq - 0 7")

print(evaluate(board,'b'))

board = chess.Board(fen='r3k2r/ppp2ppp/2nq1n2/2PpB3/6b1/2N2N1P/PPP1PPP1/R2QKB1R w KQkq - 1 8')

print(evaluate(board,'b'))
board = chess.Board(fen='r3k2r/ppp2ppp/2nP1n2/3pB3/6b1/2N2N1P/PPP1PPP1/R2QKB1R b KQkq - 0 8')

print(evaluate(board,'b'))'''