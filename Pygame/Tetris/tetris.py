import pygame
import random

# GLOBALS VARIABLES (Board is 10 x 20 Blocks)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 675
BLOCK_SIZE = 30
GAME_WIDTH = 300  # 10 * 30 = 300
GAME_HEIGHT = 600  # 20 * 30 = 600
 
TOPLEFT_WIDTH = (SCREEN_WIDTH - GAME_WIDTH) // 2
TOPLEFT_HEIGHT = SCREEN_HEIGHT - GAME_HEIGHT

# SHAPE FORMATS
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# Index 0 - 6 Represent Shapes
shapes = [S, Z, I, O, J, L, T]
shape_colours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# How Tetris Works:

# PART 1: INITIALIZATION:
# A list contains every shape
# Each individual shape is another list of formats with different rotations
# The grid is a 2D list with colours (black = empty)
# A locked position dictionary also contains colours mapped to locked positions
# Each piece is an object with a position and rotation
# Note: The locked positions dictionary contains the pieces that have hit the ground
#       The grid list contains previous pieces and the current piece

# PART 2: DRAWING THE WINDOW
# The grid is reset and updated with locked positions (create_grid)
# The grid is updated with the positions of the current piece
# The window is updated using the colours in the grid 2D list (draw_window)

# PART 3: MOVEMENT
# When a key is pressed, the piece's rotation or position is changed
# Every tick, the piece's position is also changed
# A list of new positions is obtained using the updated piece (new_positions)
# If the new positions are valid, the grid is updated (is_valid)

# PART 4: CHANGING PIECES
# If piece cannot move down anymore, the piece has hit the ground
# The locked dictionary is updated with the all the positions of the piece
# The piece is changed into a random piece (get_shape)

# PART 5: CLEARING A ROW (clear_rows)
# If a whole row is not empty, the row is deleted from the locked dictionary
# Every row above is shifted down a row


# Object for Each Tetris Piece
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.colour = shape_colours[shapes.index(shape)]
        self.rotation = 0
    
    def reset(self):
        self.x = 5
        self.y = 0


# Updates Grid Based on Locked Positions
def create_grid(locked={}):
    # Create Empty Grid
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    
    # Change Colours on Grid
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if (c, r) in locked:
                colour = locked[(c, r)]
                grid[r][c] = colour
    return grid


# Obtains New Positions After Change in Block Format
def new_positions(piece):
    positions = []

    # Shape Format for Specified Rotation
    format = piece.shape[piece.rotation % len(piece.shape)]

    # Add Positions of Blocks to List
    for i, line in enumerate(format):
        r = list(line)
        for j, c in enumerate(r):
            if c == "0":
                positions.append((piece.x + j, piece.y + i))
    
    # Adjust to Match
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    
    return positions


# Determines If Shape is in a Valid Space
def valid_space(shape, grid):
    # Accepted Positions
    accept = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accept = [j for sub in accept for j in sub]

    # New Positions
    positions = new_positions(shape)

    # Compare New and Accepted Positions
    for pos in positions:
        if pos not in accept and pos[1] > -1:
            return False
    return True


# Checks for Game Over
def check_lost(positions):
    for pos in positions:
        _, y = pos
        if y < 1:
            return True
    return False


# Obtains Random Shape
def get_shape():
    return Piece(5, 0, random.choice(shapes))


# Draws Game Over Text
def draw_text_middle(surface, text, size, colour):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    lbl = font.render(text, 1, colour)

    surface.blit(lbl, (TOPLEFT_WIDTH + GAME_WIDTH/2 - lbl.get_width()/2, TOPLEFT_HEIGHT + GAME_HEIGHT/2 - lbl.get_height()/2))


# Clears Blocks After Full Row
def clear_rows(grid, locked):
    inc = 0

    # Delete Full Row
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            index = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    
    # Shift Every Row Down
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:  # for every row from top to bottom
            x, y = key
            if y < index:  # if row is above deleted row
                newKey = (x, y + inc)  # find new position of row
                locked[newKey] = locked.pop(key)  # change to new position of row
    
    return inc


# Shows Next Shape
def draw_sidebar(surface, piece, score, high_score):
    sx = TOPLEFT_WIDTH + GAME_WIDTH + 50
    sy = TOPLEFT_HEIGHT + GAME_HEIGHT/2 - 100

    # Draw Label
    font = pygame.font.SysFont('comicsans', 20)
    lbl = font.render('Next Shape', 1, (255,255,255))
    surface.blit(lbl, (sx + 15, sy - 50))

    # Draw Score
    lbl = font.render('Score: ' + str(score), 1, (255,255,255))
    surface.blit(lbl, (sx + 30, sy + 160))

    # Draw High Score
    lbl = font.render('High Score: ' + str(high_score), 1, (255,255,255))
    surface.blit(lbl, (sx - 550, sy + 160))

    # Draw Next Shape
    format = piece.shape[0]
    for i, line in enumerate(format):
        r = list(line)
        for j, c in enumerate(r):
            if c == "0":
                pygame.draw.rect(surface, piece.colour, (sx + j*BLOCK_SIZE, sy + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)    


# Update High Score With New Score
def update_score(score):
    high_score = int(get_high_score())
    
    with open('Tetris\scores.txt', 'w') as f: 
        if high_score > score:
            f.write(str(high_score))
        else:
            f.write(str(score))


# Obtain High Score
def get_high_score():
    with open('Tetris\scores.txt', 'r') as f: 
        lines = f.readlines()
        score = lines[0].strip()
    
    return score


# Draw and Update Window
def draw_window(surface, grid):
    surface.fill((0,0,0))

    # Draw Label
    sx = TOPLEFT_WIDTH
    sy = TOPLEFT_HEIGHT
    font = pygame.font.SysFont('comicsans', 50)
    lbl = font.render('Tetris', 1, (255,255,255))
    surface.blit(lbl, (sx + GAME_WIDTH/2 - lbl.get_width()/2, 0))

    # Draw Squares
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            pygame.draw.rect(surface, grid[r][c], (sx + c*BLOCK_SIZE, sy + r*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    
    # Draw Gridlines
    for r in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + r*BLOCK_SIZE), (sx + GAME_WIDTH, sy + r*BLOCK_SIZE))
        for c in range(len(grid[r])):
            pygame.draw.line(surface, (128,128,128), (sx + c*BLOCK_SIZE, sy), (sx + c*BLOCK_SIZE, sy + GAME_HEIGHT))
    
    # Draw Border
    pygame.draw.rect(surface, (255,0,0), (sx, sy, GAME_WIDTH, GAME_HEIGHT), 4)


def main(window):
    # Create Grid and Locked Positions List
    locked = {}
    grid = create_grid(locked)

    # Initialize Variables
    change_piece = False
    run = True

    piece = get_shape()
    next_piece = get_shape()

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0

    score = 0
    count = 0

    while run:
        # Creates Grid
        grid = create_grid(locked)

        # Makes Blocks Fall
        fall_time += clock.get_rawtime()

        if fall_time/1000 > fall_speed:
            fall_time = 0
            piece.y += 1
            if not(valid_space(piece, grid)) and piece.y > 0:
                piece.y -= 1
                change_piece = True

        # Makes Blocks Fall Faster After Time
        level_time += clock.get_rawtime()
        clock.tick()

        # if level_time/1000 > 10:
        #     level_time = 0
        #     if fall_speed > 0.12:
        #         fall_speed -= 0.01

        # Checks for Key Presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece.x -= 1
                    if not(valid_space(piece, grid)):
                        piece.x += 1
                if event.key == pygame.K_RIGHT: 
                    piece.x += 1
                    if not(valid_space(piece, grid)):
                        piece.x -= 1
                if event.key == pygame.K_DOWN:
                    piece.y += 1
                    if not(valid_space(piece, grid)):
                        piece.y -= 1
                if event.key == pygame.K_UP:
                    piece.rotation += 1
                    if not(valid_space(piece, grid)):
                        piece.rotation -= 1
                if event.key == pygame.K_SPACE:
                    while valid_space(piece, grid):
                        piece.y += 1
                    piece.y -= 1
                if event.key == pygame.K_c and count == 0:
                    temp = piece
                    piece = next_piece
                    next_piece = temp
                    piece.reset()
                    next_piece.reset()
                    count += 1
        
        # Updates Colours of New Positions
        shape_pos = new_positions(piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = piece.colour
        
        # Changes to New Piece
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked[p] = piece.colour
            piece = next_piece
            next_piece = get_shape()
            change_piece = False
            count = 0
            score += 10 * clear_rows(grid, locked)
        
        # Update Score
        update_score(score)
        high_score = get_high_score()

        # Draws Window
        draw_window(window, grid)
        draw_sidebar(window, next_piece, score, high_score)
        pygame.display.update()

        # Check for Game Over
        if check_lost(locked):
            draw_text_middle(window, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

    # Return to Main Menu After Game Over
    main_menu()
 

# Open Main Menu
def main_menu():
    # Initiate Window
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    pygame.font.init()

    run = True
    while run:
        # Draw Label
        window.fill((0,0,0))
        draw_text_middle(window, 'Press Any Key to Play', 60, (255,255,255))
        pygame.display.update()
        
        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            # Start Game
            if event.type == pygame.KEYDOWN:
                main(window)


# Start Program
main_menu()