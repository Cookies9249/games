import pygame
from settings import *
from support import import_folder
from random import randint, choice
from timer_class import Timer

# objects are drawn in custom_draw in CameraGroup
class Generic(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos, layer_order=LAYERS['main'], name=''):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.layer_order = layer_order
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
        self.name = name

class Fence(Generic):
    def __init__(self, groups, surf, pos):
        super().__init__(groups, surf, pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.height * 0.6, -self.rect.height * 0.8)

class Water(Generic):
    def __init__(self, groups, pos):
        self.frames = import_folder('graphics/water')
        self.frame_index = 0

        super().__init__( 
            groups=groups,
            surf=self.frames[self.frame_index],
            pos=pos,
            layer_order=LAYERS['water'])
    
    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self, dt):
        self.animate(dt)

class Wildflower(Generic):
    def __init__(self, groups, surf, pos):
        super().__init__(groups, surf, pos)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

class Tree(Generic):
    def __init__(self, groups, surf, pos, tree_size, update_inventory):
        super().__init__(groups, surf, pos)
        self.update_inventory = update_inventory
        self.axe_sound = pygame.mixer.Sound('audio/axe.wav')

        # tree
        self.health = 5
        self.tree_alive = True
        self.stump = pygame.image.load(f'graphics/stumps/{tree_size.lower()}.png')

        # apple
        self.apple = pygame.image.load('graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[tree_size]
        self.apples = pygame.sprite.Group()
        self.create_fruit()

    def damage(self):
        # damage
        self.health -= 1
        self.axe_sound.play()

        # remove apple
        if len(self.apples.sprites()) > 0:
            random_apple = choice(self.apples.sprites())
            Particle(
                groups=self.groups()[0],
                surf=random_apple.image,
                pos=random_apple.rect.topleft,
                layer_order=LAYERS['fruit'],
                duration=200)
            random_apple.kill()
            self.update_inventory('apple', 1)
        
        # no more health
        if self.health <= 0:
            self.tree_alive = False
            Particle(
                groups=self.groups()[0],
                surf=self.image,
                pos=self.rect.topleft,
                layer_order=LAYERS['main'] + 1, # on purpose
                duration=300)
            self.image = self.stump
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.9)
            self.hitbox.centery -= 29
            self.update_inventory('wood', randint(1,3))

    def create_fruit(self):
        for pos in self.apple_pos:
            if not randint(0, 5):
                Generic(
                    groups=[self.apples, self.groups()[0]], # apple_sprites and sprites
                    surf=self.apple,
                    pos=(self.rect.left + pos[0], self.rect.top + pos[1]),
                    layer_order=LAYERS['fruit'])

class Particle(Generic):
    def __init__(self, groups, surf, pos, layer_order, duration):
        super().__init__(groups, surf, pos, layer_order)
        self.timer = Timer(duration, self.kill)
        self.timer.activate()

        mask = pygame.mask.from_surface(self.image)
        new_surf = mask.to_surface()
        new_surf.set_colorkey((0,0,0))
        self.image = new_surf
    
    def update(self, dt):
        self.timer.update()            

class Interactor(Generic):
    def __init__(self, groups, size, pos, name):
        surf = pygame.Surface(size)
        super().__init__(groups, surf, pos)
        self.name = name