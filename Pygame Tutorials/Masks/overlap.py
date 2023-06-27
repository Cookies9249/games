import pygame, sys
from framerate import debug
import time

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

player_surf = pygame.image.load('assets/alpha.png').convert_alpha()
player_surf = pygame.transform.rotozoom(player_surf, 0, 0.2)
player_rect = player_surf.get_rect(center = (300,300))
player_mask = pygame.mask.from_surface(player_surf)

obstacle_surf = pygame.image.load('assets/alpha.png').convert_alpha()
obstacle_surf = pygame.transform.rotozoom(obstacle_surf, 0, 0.8)
obstacle_rect = obstacle_surf.get_rect(center = (300,300))
obstacle_mask = pygame.mask.from_surface(obstacle_surf)

small_surf = pygame.image.load('assets/alpha.png').convert_alpha()
small_surf = pygame.transform.rotozoom(small_surf, 0, 0.4)
small_mask = pygame.mask.from_surface(small_surf)
small_rect = small_surf.get_rect(center = (400,300))

def collision(rect1, rect2, mask1, mask2, color):
    offset_x = rect2.left - rect1.left
    offset_y = rect2.top - rect1.top

    if mask1.overlap(mask2, (offset_x,offset_y)):
        mask = mask1.overlap_mask(mask2, (offset_x,offset_y))
        mask_surf = mask.to_surface()
        mask_surf.set_colorkey((0,0,0))
        mask_surf.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        screen.blit(mask_surf, rect1)
        return mask

small_dx = 3
small_dy = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('white')

	# display obstacle 
    screen.blit(obstacle_surf, obstacle_rect)

    # display small
    if small_rect.left <= 0 or small_rect.right >= 600:
        small_dx *= -1
    if small_rect.top <= 0 or small_rect.bottom >= 600:
        small_dy *= -1
    small_rect.x += small_dx
    small_rect.y += small_dy

    screen.blit(small_surf, small_rect)
	
	# display player
    if pygame.mouse.get_pos():
        player_rect.center = pygame.mouse.get_pos()
    screen.blit(player_surf, player_rect)

    # collisions
    mask1 = collision(player_rect, obstacle_rect, player_mask, obstacle_mask, 'red')
    collision(player_rect, small_rect, player_mask, small_mask, 'green')
    collision(small_rect, obstacle_rect, small_mask, obstacle_mask, 'blue')
    
    # collision all
    if mask1:
        collision(player_rect, small_rect, mask1, small_mask, 'yellow')

    pygame.display.update()
    clock.tick(60)