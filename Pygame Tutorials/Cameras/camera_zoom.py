import pygame, sys
from random import randint
import time
from framerate import debug

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
        self.speed = 400
    
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

        # zoom
        self.zoom = 1
        self.inner_size = (1536,960)
        self.inner_surf = pygame.Surface(self.inner_size, pygame.SRCALPHA)
        self.inner_rect = self.inner_surf.get_rect(center = (self.width/2, self.height/2))
        self.inner_vector = pygame.math.Vector2(self.inner_size)
        self.inner_offset = pygame.math.Vector2()
        self.inner_offset.x = (self.inner_size[0] - self.width) / 2
        self.inner_offset.y = (self.inner_size[1] - self.height) / 2
    
    def center_target_camera(self, player):
        # gets position of the TOPLEFT of screen
        self.offset.x = player.rect.centerx - self.width / 2
        self.offset.y = player.rect.centery - self.height / 2
    
    def zoom_mouse(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                camera_group.zoom += event.y * 0.03
        
        if self.zoom < 0.67: self.zoom = 0.67
        if self.zoom > 2: self.zoom = 2
        
    def custom_draw(self, player):
        self.zoom_mouse()
        self.center_target_camera(player)

        debug(f'zoom: {self.zoom}')
        self.inner_surf.fill('#71ddee')

        # get distance between 
        ground_offset = self.ground_rect.topleft - self.offset + self.inner_offset
        self.inner_surf.blit(self.ground, ground_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset + self.inner_offset
            self.inner_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.inner_surf, self.inner_vector * self.zoom)
        scaled_rect = scaled_surf.get_rect(center = (self.width/2, self.height/2))
        
        self.surface.blit(scaled_surf, scaled_rect)
 
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
        if event.type == pygame.MOUSEWHEEL:
            camera_group.zoom += event.y * 0.03
    
    screen.fill('#71ddee')

    # deltatime
    dt = time.time() - last_time
    last_time = time.time()

    # draw on screen
    camera_group.update(dt)
    camera_group.custom_draw(player)
    
    pygame.display.update()
    clock.tick(60)
    