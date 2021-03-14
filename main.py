import display
import pygame, sys, chess
import copy
import random
import random_agent
import player_agent
import minimax_agent
import pandas as pd
print('a')
import matplotlib.pyplot as plt
import minimax_agent_2
print('b')
import datetime
import time
import numpy as np
from pygame.locals import *

board = chess.Board()

pygame.init()



def to_play(board):
    return board.fen().split(' ')[1]

def play_game(agent_w, agent_b, pov, show=True, print_moves=True):
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
                move = agent_w.get_move(board)
                white_move_arr.append(str(move))
                old_time, new_time = new_time, datetime.datetime.now()
                white_time_arr.append((new_time - old_time).total_seconds())
                #print('white time: ', white_time_arr[-1])
            else:
                move = agent_b.get_move(board)
                old_time, new_time = new_time, datetime.datetime.now()
                black_time_arr.append((new_time - old_time).total_seconds())
                black_move_arr.append(str(move))
                san_arr.append(temp_board.variation_san([chess.Move.from_uci(m) for m in [white_move_arr[-1],
                                                                                      black_move_arr[-1]]]))

                if print_moves:
                    print(san_arr[-1])

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

#result = play_game(minimax_agent.MinimaxAgent(2, square_weighting=True), minimax_agent.MinimaxAgent(2), pov='w', show=True)


weight_agent = minimax_agent_2.MinimaxAgent(1)
no_weight_agent = minimax_agent.MinimaxAgent(1, ratio=True, square_weighting=True)


game_count = 100

weight_wins = 0
no_weight_wins = 0
for i in range(game_count):
    if i % 2 == 0:
        result = play_game(weight_agent, no_weight_agent, pov='w',
                       show=False, print_moves=False)
    else:
        result = play_game(no_weight_agent, weight_agent, pov='w', show=False, print_moves=False)
    print('result', result[0])

    if result[0] == '1-0':
        if i % 2 == 0:
            weight_wins += 1
        elif i % 2 == 1:
            no_weight_wins += 1
    elif result[0] == '0-1':
        if i % 2 == 0:
            no_weight_wins += 1
        else:
            weight_wins += 1
    print(weight_wins, '-', no_weight_wins)



