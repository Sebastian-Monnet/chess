import chess

def prioritise(move_arr):
    high, low = [], []
    for move in move_arr:
        if 'x' in str(move):
            high.append('move')
        else:
            low.append('move')