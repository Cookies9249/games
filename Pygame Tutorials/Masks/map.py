import pygame, sys
from framerate import debug

SCREEN_SIZE = 600
CUBE_SIZE = 400
PLAYER_SIZE = 10
CENTER = (SCREEN_SIZE/2, SCREEN_SIZE/2)
MARGIN = (SCREEN_SIZE-CUBE_SIZE)/2

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
clock = pygame.time.Clock()
screen.fill('white')

player_surf = pygame.Surface((PLAYER_SIZE,PLAYER_SIZE))
player_surf.fill('red')
player_rect = player_surf.get_rect(center = CENTER)
player_mask = pygame.mask.from_surface(player_surf)

#
last_player_rect = player_rect.copy()
last_player_mask = player_mask.copy()

# obstacle_surf = pygame.Surface((CUBE_SIZE,CUBE_SIZE))
obstacle_surf = pygame.image.load('assets/alpha.png')
obstacle_surf = pygame.transform.rotozoom(obstacle_surf, 0, 0.8)
obstacle_rect = obstacle_surf.get_rect(center = CENTER)
obstacle_mask = pygame.mask.from_surface(obstacle_surf)

def test():
    global last_player_mask, last_player_rect

    screen.fill('white')

	# obstacle 
    screen.blit(obstacle_surf, obstacle_rect)
	
	# moving part
    if pygame.mouse.get_pos():
        player_rect.center = pygame.mouse.get_pos()

    # collision
    offset_x = obstacle_rect.left - player_rect.left
    offset_y = obstacle_rect.top - player_rect.top
    if not player_mask.overlap_area(obstacle_mask, (offset_x,offset_y)) == PLAYER_SIZE**2:
        # if last_player_mask.overlap_area(obstacle_mask, (offset_x,offset_y)) == PLAYER_SIZE**2:
        player_rect.topleft = last_player_rect.topleft
    
        # FOR RECTANGLES
        # if player_rect.left < MARGIN: player_rect.left = MARGIN
        # if player_rect.right > SCREEN_SIZE-MARGIN: player_rect.right = SCREEN_SIZE-MARGIN
        # if player_rect.top < MARGIN: player_rect.top = MARGIN
        # if player_rect.bottom > SCREEN_SIZE-MARGIN: player_rect.bottom = SCREEN_SIZE-MARGIN

    screen.blit(player_surf, player_rect)
    last_player_rect = player_rect.copy()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
    test()

    # WENT TO TEST
        

    pygame.display.update()
    clock.tick(60)