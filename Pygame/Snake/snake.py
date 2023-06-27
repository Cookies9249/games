import random
import pygame
import tkinter
from tkinter import messagebox

# How Snake Works (Movement):
# - The snake is a list of cube objects
# - The snake has a dictionary of positions mapped to turns
# - Each cube object in the snake has a position and direction
# - When the snake moves, each individual cube changes its position based on direction
# - If the cube is on a position mapped to a turn, the direction changes
# - Every frame, the window is drawn based on the position of cubes

# How Snake Works (Gameplay):
# - If the snake hits a snack, a new cube is added at the end of the snake
# - If the snake hits itself, the game is over


# Create an object for every cube
class cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dx=1, dy=0, color=(255, 0, 0)):
        self.pos = start
        self.dx = dx
        self.dy = dy
        self.color = color

    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)

    # Draw the cube on the window
    def draw(self, surface):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        # Draw cube based on position
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

# Create an object for the whole snake
class snake(object):
    body = []   # List of cube objects in snake
    turns = {}  # Dictionary of position and turns

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dx = 0
        self.dy = 1

    def move(self):
        # Move the snake based on pressed keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.dx = -1
                self.dy = 0

                # Add turn into dictionary mapped to position
                self.turns[self.head.pos] = [-1, 0]

            elif keys[pygame.K_RIGHT]:
                self.dx = 1
                self.dy = 0
                self.turns[self.head.pos] = [1, 0]

            elif keys[pygame.K_UP]:
                self.dx = 0
                self.dy = -1
                self.turns[self.head.pos] = [0, -1]

            elif keys[pygame.K_DOWN]:
                self.dx = 0
                self.dy = 1
                self.turns[self.head.pos] = [0, 1]
        
        # For every cube in snake
        for i, c in enumerate(self.body):
            # Get position of cube
            p = c.pos[:]
            # If the position is mapped to a turn
            if p in self.turns:
                # Change direction
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # If snake is at end of board
                if c.dx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dy == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dy == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)

                # Otherwise, move the snake
                else: c.move(c.dx, c.dy)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dx = 0
        self.dy = 1

    # Add a new cube to the snake
    def addCube(self):
        tail = self.body[-1]
        dx = tail.dx
        dy = tail.dy
        
        # Add new cube to position behind tail cube
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        # Set direction of new cube
        self.body[-1].dx = dx
        self.body[-1].dy = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface)

# Draw gridlines
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x, y = 0, 0

    for i in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y))

# Redraw window every frame
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

# Spawn in a random snack
def randomSnack(item):
    global rows
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        
        if len(list(filter(lambda z:z.pos == (x,y), positions))) == 0:
            break
    return (x,y)


def messageBox(subject, content):
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    # Initialize
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(s), color=(0,255,0))
    
    clock = pygame.time.Clock()

    while True:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()

        # If snake eats a snack
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(s), color=(0,255,0))

        # If snake hits itself
        for x in range(len(s.body)):
            # If the position of two cubes are the same
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                messageBox('You Lost!', f'Score: {len(s.body)}')
                s.reset((10,10))
                break

        redrawWindow(win)


main()