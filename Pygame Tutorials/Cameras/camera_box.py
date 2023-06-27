import pygame, sys
from random import randint
import time

WIDTH = 1024
HEIGHT = 640

class Tree(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pos ##

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pos
        self.direction = pygame.math.Vector2()
        self.speed = 300
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: 
            self.direction.y = -1
        elif keys[pygame.K_DOWN]: 
            self.direction.y = 1
        else: 
            self.direction.y = 0
        if keys[pygame.K_RIGHT]: 
            self.direction.x = 1
        elif keys[pygame.K_LEFT]: 
            self.direction.x = -1
        else: 
            self.direction.x = 0

    def update(self, dt):
        self.input()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # update position
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = self.pos

class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.surface = pygame.display.get_surface()
        
        # ground
        self.ground = pygame.image.load('graphics/ground.png').convert_alpha()
        self.ground = pygame.transform.rotozoom(self.ground, 0, 0.8)
        self.ground_rect = self.ground.get_rect(center = (WIDTH/2, HEIGHT/2))
        
        # camera
        self.offset = pygame.math.Vector2()
        self.width = self.surface.get_size()[0]
        self.height = self.surface.get_size()[1]

        ################################### box setup ###################################
        self.l, self.t = (200, 100)
        w = self.width - self.l * 2
        h = self.height - self.t * 2
        self.camera_rect = pygame.Rect(self.l, self.t, w, h)
    
    def box_target_camera(self, player):
        # move box with player
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        # gets position of the TOPLEFT of screen
        self.offset.x = self.camera_rect.left - self.l
        self.offset.y = self.camera_rect.top - self.t

    def custom_draw(self, dt, player):
        self.box_target_camera(player)

        # get distance between 
        ground_offset = self.ground_rect.topleft - self.offset
        self.surface.blit(self.ground, ground_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset
            self.surface.blit(sprite.image, offset_pos)
        
        pygame.draw.circle(self.surface, 'red', (0,0), 20)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

camera_group = CameraGroup()

# Player
player = Player(camera_group, (WIDTH/2, HEIGHT/2))

# Trees
for i in range(20):
    x = randint(-900, 900)
    y = randint(-600, 600)
    Tree(camera_group, (x,y))

last_time = time.time()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('#71ddee')

    # deltatime
    dt = time.time() - last_time
    last_time = time.time()

    # draw on screen
    camera_group.update(dt)
    camera_group.custom_draw(dt, player)
    
    pygame.display.update()
    clock.tick(60)
    