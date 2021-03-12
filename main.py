import display
import pygame, sys, chess
import copy
import random
import random_agent
import player_agent
import minimax_agent
print('a')
import matplotlib.pyplot as plt
print('b')
import datetime
import time
import numpy as np
from pygame.locals import *

board = chess.Board()

pygame.init()



def to_play(board):
    return board.fen().split(' ')[1]

def play_game(agent_w, agent_b, pov, show=True):
    board = chess.Board()
    if show:
        screen = pygame.display.set_mode((display.BOARD_LENGTH + 2 * display.BORDER,
                                          display.BOARD_LENGTH + 2 * display.BORDER), 0, 32)
        display.draw_board(screen)

    new_time = datetime.datetime.now()
    white_time_arr = []
    black_time_arr = []
    san_arr = []
    white_move_arr = []
    black_move_arr = []

    while not board.is_game_over():
        if not board.is_game_over():
            turn = to_play(board)

            if turn=='w':
                temp_board = copy.deepcopy(board)
                move = agent_w.get_move(board, turn)
                white_move_arr.append(str(move))
                old_time, new_time = new_time, datetime.datetime.now()
                white_time_arr.append((new_time - old_time).total_seconds())
                #print('white time: ', white_time_arr[-1])
            else:
                move = agent_b.get_move(board, turn)
                old_time, new_time = new_time, datetime.datetime.now()
                black_time_arr.append((new_time - old_time).total_seconds())
                black_move_arr.append(str(move))
                san_arr.append(temp_board.variation_san([chess.Move.from_uci(m) for m in [white_move_arr[-1],
                                                                                      black_move_arr[-1]]]))
                #print(san_arr[-1])

                #print('black time: ', black_time_arr[-1])
            board.push_uci(move)

            if show:
                display.draw_board(screen)
                display.draw_all_pieces(board.fen(), screen, pov)
                pygame.display.update()

        if show:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

    if show:
        running = True
        while running:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    running = False


    return board.result(), white_time_arr, black_time_arr, san_arr

#result = play_game(screen, player_agent.PlayerAgent(), random_agent.RandomAgent(), pov='w')

games = 1
white_arr = - np.ones((games, 300))
black_arr = - np.ones((games, 300))

for i in range(games):
    result, white_times, black_times, san_arr = play_game(minimax_agent.MinimaxAgentIter(1),
                                                  minimax_agent.MinimaxAgentRecur(0), pov='w', show=False)
    white_arr[i][:len(white_times)] = white_times
    black_arr[i][:len(black_times)] = black_times

print(white_arr)
white_arr = np.array(white_arr)
black_arr = np.array(black_arr)

to_plot_white = np.zeros(100)
to_plot_black = np.zeros(100)
for i in range(100):
    to_plot_white[i] = np.mean(white_arr[:, i][white_arr[:,i] != -1])
    to_plot_black[i] = np.mean(black_arr[:, i][black_arr[:, i] != -1])


#print(result)
plt.plot(to_plot_white, label='white')
plt.plot(to_plot_black, label='black')
plt.legend()
plt.show()
