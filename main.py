import display
import pygame, sys, chess
import random
import random_agent
import player_agent
import time
from pygame.locals import *

board = chess.Board()

pygame.init()

screen = pygame.display.set_mode((display.BOARD_LENGTH + 2 * display.BORDER,
                                  display.BOARD_LENGTH + 2 * display.BORDER), 0, 32)

def to_play(board):
    return board.fen().split(' ')[1]

def play_game(screen, agent_w, agent_b, pov):
    board = chess.Board()
    display.draw_board(screen)

    while not board.is_game_over():
        if not board.is_game_over():
            turn = to_play(board)
            if turn=='w':
                move = agent_w.get_move(board, turn)
            else:
                move = agent_b.get_move(board, turn)
            board.push_uci(move)

            print(board)


            display.draw_board(screen)
            display.draw_all_pieces(board.fen(), screen, pov)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

        time.sleep(0.2)

    return board.result()

result = play_game(screen, player_agent.PlayerAgent(), random_agent.RandomAgent(), pov='w')
#result = play_game(screen, random_agent.RandomAgent(), random_agent.RandomAgent(), pov='w')
print(result)