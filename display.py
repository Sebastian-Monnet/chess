import pygame, sys, chess
from pygame.locals import *

BOARD_LENGTH = 640
BORDER = 20
SQUARE_LENGTH = BOARD_LENGTH // 8

DARK_SQUARE = (50, 50, 100)
LIGHT_SQUARE = (50, 50, 200)

LETTER_TO_NUM = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
NUM_TO_LETTER = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}


def notation_to_coord(notation, pov='w'):
    a, b = notation
    x = LETTER_TO_NUM[a] - 1
    if pov == 'w':
        y = 8 - int(b)
    else:
        y = int(b) - 1

    return x, y


def draw_board(screen):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 1:
                colour = DARK_SQUARE
            else:
                colour = LIGHT_SQUARE

            pygame.draw.rect(screen, colour,
                             (BORDER + i * SQUARE_LENGTH, BORDER + j * SQUARE_LENGTH, SQUARE_LENGTH, SQUARE_LENGTH))


def get_piece_img(piece_name):
    '''
    :param piece_name: character. Uppercase = white, lowercase = black.
    :return: Image of piece.
    '''
    if piece_name.isupper():
        colour = 'w'
    else:
        colour = 'b'
    filename = colour + piece_name.lower()
    return pygame.image.load('sprites/' + filename + '.png')

def draw_piece(screen, pos, piece_name, pov='w'):
    '''
    :param screen: pygame display object
    :param pos: string. Piece position in chess notation, e.g. 'e4'
    :param piece_name: string. Piece name. Lowercase=black, uppercase=white.
    :return: None
    '''
    a, b = notation_to_coord(pos, pov=pov)
    img = get_piece_img(piece_name)
    img = pygame.transform.scale(img, (SQUARE_LENGTH, SQUARE_LENGTH))
    rect = (BORDER + a * SQUARE_LENGTH, BORDER + b * SQUARE_LENGTH, SQUARE_LENGTH, SQUARE_LENGTH)
    screen.blit(img, rect)


def draw_FEN_row(row_str, rank, screen, pov='w'):
    '''
    :param row_str: string. FEN representation of row.
    :param screen: pygame screen.
    :param rank: int between 1 and 8 inclusive.
    :param pov: string
    :return:
    '''
    current_file = 1
    for char in row_str:
        if char.isalpha():
            pos = NUM_TO_LETTER[current_file] + str(rank)
            draw_piece(screen, pos, char, pov=pov)
            current_file += 1
        else:
            current_file += int(char)


def draw_all_pieces(gamestate, screen, pov):
    '''
    :param gamestate: string. FEN representation of gamestate.
    :param screen: pygame screen.
    :param pov: char
    :return:
    '''
    row_arr = gamestate.split('/')
    row_arr[-1] = row_arr[-1].split(' ')[0]
    for i, row in enumerate(row_arr):
        draw_FEN_row(row, 8-i, screen, pov)



def main():
    pygame.init()

    screen = pygame.display.set_mode((BOARD_LENGTH + 2 * BORDER, BOARD_LENGTH + 2 * BORDER), 0, 32)

    draw_board(screen)

    board = chess.Board()

    draw_all_pieces(board.fen(), screen, 'w')




    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


