import display
import pygame, sys, chess
import copy
import random
import random_agent
import player_agent
import minimax_agent
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
import minimax_agent_2
import numpy as np
import evaluation_2
from pygame.locals import *

def selected_square(x, y, pov):
    i = (x - display.BORDER) // display.SQUARE_LENGTH
    j = (y - display.BORDER) // display.SQUARE_LENGTH

    if pov == 'w':
        return display.NUM_TO_LETTER[i+1] + str(8-j)
    else:
        return display.NUM_TO_LETTER[8-i] + str(j+1)

def is_in_board(x,y):
    if not (display.BORDER < x and x <= display.BORDER + 8 * display.SQUARE_LENGTH):
        return False
    if not (display.BORDER < y and y <= display.BORDER + 8 * display.SQUARE_LENGTH):
        return False
    return True

def get_player_move(screen, board, pov):
    '''
    :param screen: pygame screen
    :param board: chess.Board() object
    :param pov: string: 'w' or 'b'. Should equal the next player to play from board.
    :return: str: move in format e.g. 'e2e4'
    '''
    is_selected = False
    while True:
        display.draw_board(screen)
        if is_selected:
            display.highlight_square(screen, piece_square, pov)
        display.draw_all_pieces(board.fen(), screen, pov)
        pygame.display.update()

        if not is_selected:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if is_in_board(x, y):
                        piece_square = selected_square(x, y, pov)
                        is_selected = True
                        break
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if is_in_board(x, y):
                        target_square = selected_square(x, y, pov)
                        legal_arr = [str(move) for move in board.legal_moves]
                        move = piece_square + target_square
                        if move in legal_arr:
                            return move
                        elif move + 'q' in legal_arr:
                            return move + 'q'
                        else:
                            is_selected = False



board = chess.Board()
screen = pygame.display.set_mode((display.BOARD_LENGTH + 2 * display.BORDER,
                                          display.BOARD_LENGTH + 2 * display.BORDER), 0, 32)

def play_game(agent, player_colour):
    board = chess.Board()

    screen = pygame.display.set_mode((display.BOARD_LENGTH + 2 * display.BORDER,
                                          display.BOARD_LENGTH + 2 * display.BORDER), 0, 32)

    san_arr = []

    while not board.is_game_over():
        turn = board.fen().split(' ')[1]
        if turn == player_colour:
            move = get_player_move(screen, board, player_colour)
        else:
            move = agent.get_move(board)
        if turn == 'w':
            temp_board = copy.deepcopy(board)
            white_move = move
        else:
            black_move = move
            san_arr.append(temp_board.variation_san([chess.Move.from_uci(m) for m in [white_move, black_move]]))
            print(san_arr[-1])
        board.push_uci(move)


        display.draw_board(screen)
        display.draw_all_pieces(board.fen(), screen, player_colour)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    while True:
        display.draw_board(screen)
        display.draw_all_pieces(board.fen(), screen, player_colour)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()




agent = minimax_agent_2.MinimaxAgent(2)

#agent = random_agent.RandomAgent()

play_game(agent, 'w')
