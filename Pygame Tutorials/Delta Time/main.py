import time
import pygame, sys
from framerate import debug

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()

test_rect = pygame.Rect(0,310,100,100)
test_speed = 200
rect_x = test_rect.x

previous_time = time.time()
while True:
    dt = time.time() - previous_time
    previous_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('white')
    debug(dt)

    rect_x += test_speed * dt
    test_rect.x = round(rect_x)
    pygame.draw.rect(screen, 'red', test_rect)

    pygame.display.update()
    clock.tick(60)

