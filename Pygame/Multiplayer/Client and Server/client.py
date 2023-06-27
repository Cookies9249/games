import pygame
from network import Network

WIDTH = 500
HEIGHT = 500

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


# Create object for player
class Player(object):
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = (x, y, width, height)
        self.vel = 3
    
    def draw(self):
        pygame.draw.rect(window, self.colour, self.rect)
    
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        self.update()
    
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


# Redraw display
def redraw_window(player, player2):
    window.fill((255,255,255))
    player.draw()
    player2.draw()
    pygame.display.update()


# Convert from string to tuple
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


# Conver from tuple to string
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


# Start game
def main():
    run = True

    # Initialize network
    n = Network()
    startPos = read_pos(n.get_pos())
    p = Player(startPos[0], startPos[1], 20, 20, (0,255,0))
    p2 = Player(0, 0, 20, 20, (255,0,0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))  # move p2
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()  # move p1

        redraw_window(p, p2)


# Start program
main()