import pygame
from settings import *
from sprites import Generic
from support import import_folder
from random import randint, choice
from timer_class import Timer

class Rain:
    def __init__(self, all_sprites) -> None:
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('graphics/rain/drops')
        self.rain_floor = import_folder('graphics/rain/floor')

        self.map_w, self.map_h = pygame.image.load('graphics/world/ground.png').get_size()
    
    def create_floor(self):
        Raindrop(
            groups = self.all_sprites,
            surf = choice(self.rain_floor),
            pos = (randint(0, self.map_w), randint(0, self.map_h)),
            layer_order = LAYERS['rain floor'],
            moving = False)

    def create_drops(self):
        Raindrop(
            groups = self.all_sprites,
            surf = choice(self.rain_drops),
            pos = (randint(0, self.map_w), randint(0, self.map_h)),
            layer_order = LAYERS['rain drops'],
            moving = True)

    def update(self):
        self.create_floor()
        self.create_drops()

class Raindrop(Generic):
    def __init__(self, groups, surf, pos, layer_order, moving):
        super().__init__(groups, surf, pos, layer_order)

        # general setup
        self.lifetime = randint(400,500)
        self.timer = Timer(self.lifetime, self.kill)
        self.timer.activate()

        # moving
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)
    
    def update(self, dt):
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.timer.update()

class Sky:
    def __init__(self) -> None:
        self.surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255,255,255]
        self.end_color = (38,101,189)
        self.color = self.start_color.copy()
    
    def display(self, dt):
        # change colour
        for index, value in enumerate(self.end_color):
            if self.color[index] > value:
                self.color[index] -= 0.5 * dt

        # blit surface
        self.full_surf.fill(self.color)
        self.surface.blit(self.full_surf, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

    # reset color of sky after new day (level > reset)
    def reset(self):
        self.color = self.start_color.copy()
