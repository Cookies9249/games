import pygame
from random import randint

GROUND_Y = 300

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # required for sprites

        self.jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.walk = [walk1, walk2]
        self.index = 0

        self.image = self.walk[self.index]  # initialize at least an image and rect
        self.rect = self.image.get_rect(midbottom = (80,GROUND_Y))
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND_Y:
            self.gravity = -20
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y

    def animate(self):
        if self.rect.bottom == 300:
            self.index += 0.1
            if self.index >= len(self.walk):
                self.index = 0
            self.image = self.walk[int(self.index)]
        else:
            self.image = self.jump
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        self.index = 0
        if type == 'fly':
            fly1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            y_pos = 200
        else:
            snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail1, snail2]
            y_pos = 300
        
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))
    
    def animate(self):
        self.index += 0.1
        
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]
    
    def destroy(self):
        if self.rect.right == 0:
            self.kill()
    
    def update(self):
        self.animate()
        self.destroy()
        self.rect.x -= 6
        