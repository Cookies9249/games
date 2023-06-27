import pygame, sys

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

player_surf = pygame.Surface((40,40))
player_surf.fill('red')
player_rect = player_surf.get_rect(center = (300,300))
player_mask = pygame.mask.from_surface(player_surf)

obstacle_surf = pygame.image.load('assets/alpha.png').convert_alpha()
obstacle_surf = pygame.transform.rotozoom(obstacle_surf, 0, 0.8)
obstacle_mask = pygame.mask.from_surface(obstacle_surf)
obstacle_pos = (75,75)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('white')

	# obstacle 
    screen.blit(obstacle_surf, obstacle_pos)
	
	# moving part
    if pygame.mouse.get_pos():
        player_rect.center = pygame.mouse.get_pos()
    screen.blit(player_surf, player_rect)

    # collision
    offset_x = obstacle_pos[0] - player_rect.left
    offset_y = obstacle_pos[1] - player_rect.top
    if player_mask.overlap_area(obstacle_mask, (offset_x,offset_y)):
        print(player_mask.overlap_area(obstacle_mask, (offset_x,offset_y)))
    
    pygame.display.update()
    clock.tick(60)