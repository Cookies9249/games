import numpy as np
import pygame
import math

ROW_COUNT = 6
COLUMN_COUNT = 7
CONNECT = 4

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, r, c, piece):
    board[r][c] = piece

def is_valid_location(board, c):
    return board[ROW_COUNT-1][c] == 0

def next_open_row(board, c):
    for r in range(ROW_COUNT):
        if board[r][c] == 0:
            return r

def winning_move(board, piece):
    # Check Horizontal Wins
    for r in range(ROW_COUNT):
        count = 0
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT:
                return True
    
    # Check Vertical Wins
    for c in range(COLUMN_COUNT):
        count = 0
        for r in range(ROW_COUNT):
            if board[r][c] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT:
                return True
    
    # Check Diagonal (m=1) Wins
    for c in range(COLUMN_COUNT-CONNECT+1):
        count = 0
        lim = COLUMN_COUNT-c
        if ROW_COUNT < lim:
            lim = ROW_COUNT
        for i in range(lim):
            if board[i][c+i] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT:
                return True

    for r in range(1, ROW_COUNT-CONNECT+1):
        count = 0
        lim = ROW_COUNT-r
        if COLUMN_COUNT < lim:
            lim = COLUMN_COUNT
        for i in range(lim):
            if board[r+i][i] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT:
                return True

    # Check Diagonal (m=-1) Wins
    for c in range(CONNECT-1, COLUMN_COUNT):
        count = 0
        lim = c+1
        if ROW_COUNT < lim:
            lim = ROW_COUNT
        for i in range(lim):
            if board[i][c-i] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT:
                return True

    for r in range(1, ROW_COUNT-CONNECT+1):
        count = 0
        lim = ROW_COUNT-r
        if COLUMN_COUNT < lim:
            lim = COLUMN_COUNT
        for i in range(lim):
            if board[r+i][COLUMN_COUNT-i-1] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT:
                return True 

SQUARE_SIZE = 80
CIRCLE_SIZE = SQUARE_SIZE/2 - 7
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)

def draw_board(screen, board):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            if board[ROW_COUNT-r-1][c] == 1: 
                colour = RED
            elif board[ROW_COUNT-r-1][c] == 2:
                colour = YELLOW
            else:
                colour = BLACK
            pygame.draw.circle(screen, colour, ((c+0.5)*SQUARE_SIZE, (r+1.5)*SQUARE_SIZE), CIRCLE_SIZE)
    pygame.display.update()


def main():
    pygame.init
    board = create_board()
    game_over = False
    player = 1

    width = COLUMN_COUNT * SQUARE_SIZE
    height = (ROW_COUNT+1) * SQUARE_SIZE
    screen = pygame.display.set_mode((width, height))
    draw_board(screen, board)
    pygame.font.init()
    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # DROP
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                if player == 1:
                    colour = RED
                else:
                    colour = YELLOW
                pygame.draw.circle(screen, colour, (event.pos[0], SQUARE_SIZE/2), CIRCLE_SIZE)
                pygame.display.update()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                # Input
                column = math.floor(event.pos[0]/SQUARE_SIZE)

                # Drop Piece
                if is_valid_location(board, column):
                        row = next_open_row(board, column)
                        drop_piece(board, row, column, player)

                # Check for Win
                if winning_move(board, player):
                    if player == 1:
                        label = myfont.render("Red Wins!", 1, RED)
                    else:
                        label = myfont.render("Yellow Wins!", 1, YELLOW)
                    screen.blit(label, (40,10))
                    game_over = True

                player = player % 2 + 1
                draw_board(screen, board)
    pygame.time.wait(3000)

main()

