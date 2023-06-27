import pygame, sys

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

# creating obstacle
obstacle_surf = pygame.image.load('assets/alpha.png').convert_alpha()
obstacle_surf = pygame.transform.rotozoom(obstacle_surf, 0, 0.8)
obstacle_mask = pygame.mask.from_surface(obstacle_surf)
obstacle_pos = (75,75)

# turn mask into surface
new_obstacle_surf = obstacle_mask.to_surface()  # get surface
new_obstacle_surf.set_colorkey((0,0,0))  # remove black

# # filling in surface
surf_w, surf_h = new_obstacle_surf.get_size()
for x in range(surf_w):  # iternate through surface
    for y in range(surf_h):
        if new_obstacle_surf.get_at((x,y))[0] != 0:  # if a pixel is not black
            new_obstacle_surf.set_at((x,y), 'orange')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    border = 5
    screen.fill('grey')

    # border (method 2)
    screen.blit(new_obstacle_surf, (obstacle_pos[0] + border, obstacle_pos[1]))
    screen.blit(new_obstacle_surf, (obstacle_pos[0], obstacle_pos[1] + border))
    screen.blit(new_obstacle_surf, (obstacle_pos[0] - border, obstacle_pos[1]))
    screen.blit(new_obstacle_surf, (obstacle_pos[0], obstacle_pos[1] - border))
    screen.blit(new_obstacle_surf, (obstacle_pos[0] + border, obstacle_pos[1] + border))
    screen.blit(new_obstacle_surf, (obstacle_pos[0] + border, obstacle_pos[1] - border))
    screen.blit(new_obstacle_surf, (obstacle_pos[0] - border, obstacle_pos[1] + border))
    screen.blit(new_obstacle_surf, (obstacle_pos[0] - border, obstacle_pos[1] - border))

    screen.blit(obstacle_surf, obstacle_pos)

    # border (method 1)
    # for x, y in obstacle_mask.outline():
    #     x += obstacle_pos[0]
    #     y += obstacle_pos[1]
    #     pygame.draw.circle(screen, 'red', (x,y), 3)

    pygame.display.update()
    clock.tick(60)
