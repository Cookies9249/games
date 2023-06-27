import pygame
import math

pygame.init() ###

FPS = 60
WIDTH = 900
HEIGHT = 800

clock = pygame.time.Clock() ###
font = pygame.font.Font("assets/font/myFont.ttf", 32)
screen = pygame.display.set_mode((WIDTH, HEIGHT)) ###

bgs = []
banners = []
guns = []
level = 1

def draw_gun():
    mouse_pos = pygame.mouse.get_pos() ###
    gun_point = (WIDTH / 2, HEIGHT - 200)
    lasers = ['red', 'purple', 'green']
    clicks = pygame.mouse.get_pressed()

    if mouse_pos[0] != gun_point[0]:
        slope = (mouse_pos[1] - gun_point[1]) / (mouse_pos[0] - gun_point[0])
        angle = math.atan(slope)
        rotation = math.degrees(angle)
    else:
        rotation = 270

    if mouse_pos[1] < 600:
        gun = guns[level - 1]
        if mouse_pos[0] < WIDTH/2:
            gun = pygame.transform.flip(gun, True, False)
            screen.blit(pygame.transform.rotate(gun, 90 - rotation), (WIDTH/2 - 90, HEIGHT - 250))
        else:
            screen.blit(pygame.transform.rotate(gun, 270 - rotation), (WIDTH/2 - 30, HEIGHT - 250))

        if clicks[0]:
            pygame.draw.circle(screen, lasers[level - 1], mouse_pos, 5)


def main():
    for i in range(1, 4):
        bgs.append(pygame.image.load(f"assets/bgs/{i}.png")) ###
        banners.append(pygame.image.load(f"assets/banners/{i}.png"))
        guns.append(pygame.transform.scale(pygame.image.load(f"assets/guns/{i}.png"), (100,100)))

    run = True
    while run:
        clock.tick(FPS) ###
        screen.fill("black") ###
        screen.blit(bgs[level-1], (0,0)) ###
        screen.blit(banners[level-1], (0,HEIGHT-200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        draw_gun()
        
        pygame.display.update()
    pygame.quit()

main()