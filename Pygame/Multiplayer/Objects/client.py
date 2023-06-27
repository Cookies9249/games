import pygame
from network import Network
from player import Player

WIDTH = 500
HEIGHT = 500

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


# Redraw display
def redraw_window(player, player2):
    window.fill((255,255,255))
    player.draw(window)
    player2.draw(window)
    pygame.display.update()


# Start game
def main():
    run = True

    # Initialize network
    n = Network()
    p = n.get_player() #####
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p) #####

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()

        redraw_window(p, p2)


# Start program
main()