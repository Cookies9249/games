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
    
    def mouse_camera(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()
        
        border_left, border_top = (200, 100)
        border_right = self.width - border_left
        border_bottom = self.height - border_top

        if border_top < mouse.y < border_bottom:
            if mouse.x < border_left: # left
                mouse_offset_vector.x = mouse.x - border_left
                pygame.mouse.set_pos((border_left, mouse.y))
            if mouse.x > border_right: # right
                mouse_offset_vector.x = mouse.x - border_right
                pygame.mouse.set_pos((border_right, mouse.y))
        
        if border_left < mouse.x < border_right:
            if mouse.y < border_top: # top
                mouse_offset_vector.y = mouse.y - border_top
                pygame.mouse.set_pos((mouse.x, border_top))
            if mouse.y > border_bottom: # bottom
                mouse_offset_vector.y = mouse.y - border_bottom
                pygame.mouse.set_pos((mouse.x, border_bottom))
        
        # topleft
        if mouse.x < border_left and mouse.y < border_top:
            mouse_offset_vector.x = mouse.x - border_left
            mouse_offset_vector.y = mouse.y - border_top
            pygame.mouse.set_pos((border_left, border_top))

        # topright
        if mouse.x > border_right and mouse.y < border_top:
            mouse_offset_vector.x = mouse.x - border_right
            mouse_offset_vector.y = mouse.y - border_top
            pygame.mouse.set_pos((border_right, border_top))

        # bottomleft
        if mouse.x < border_left and mouse.y > border_bottom:
            mouse_offset_vector.x = mouse.x - border_left
            mouse_offset_vector.y = mouse.y - border_bottom
            pygame.mouse.set_pos((border_left, border_bottom))

        # bottomright
        if mouse.x > border_right and mouse.y > border_bottom:
            mouse_offset_vector.x = mouse.x - border_right
            mouse_offset_vector.y = mouse.y - border_bottom
            pygame.mouse.set_pos((border_right, border_bottom))

        self.offset += mouse_offset_vector

    def custom_draw(self):
        self.mouse_camera()

        # get distance between 
        ground_offset = self.ground_rect.topleft - self.offset
        self.surface.blit(self.ground, ground_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset
            self.surface.blit(sprite.image, offset_pos)
 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

camera_group = CameraGroup()
pygame.mouse.set_pos((WIDTH/2, HEIGHT/2))

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
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    
    screen.fill('#71ddee')

    # deltatime
    dt = time.time() - last_time
    last_time = time.time()

    # draw on screen
    camera_group.update(dt)
    camera_group.custom_draw()
    
    pygame.display.update()
    clock.tick(60)
    