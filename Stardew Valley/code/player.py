import pygame
from settings import *
from support import *
from timer_class import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, colliders, trees, interactors, soil, toggle_shop):
        super().__init__(group)

        # animation
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.layer_order = LAYERS['main']

        # collision
        self.hitbox = self.rect.copy().inflate((-126,-70))
        self.colliders = colliders

        # movement
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2()
        self.speed = 250

        # timers
        self.timers = {
            'tool use': Timer(500, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(500, self.use_seed),
            'seed switch': Timer(200),
            'toggle shop': Timer(200)
        }

        # tool
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]
        self.soil = soil

        # inventory
        self.inventory = {
            'wood':         0,
            'apple':        0,
            'corn':         0,
            'tomato':       0,
            'corn seed':    5,
            'tomato seed':  5
        }
        self.money = 200

        # interaction
        self.trees = trees
        self.interactors = interactors
        self.sleep = False
        self.toggle_shop = toggle_shop
    
    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_hoe': [], 'down_hoe': [], 'left_hoe': [], 'right_hoe': [],
                           'up_axe': [], 'down_axe': [], 'left_axe': [], 'right_axe': [],
                           'up_water': [], 'down_water': [], 'left_water': [], 'right_water': []}

        for animation in self.animations.keys():
            folder_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(folder_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

# (self > update)
    def input(self):
        keys = pygame.key.get_pressed()

        # movement
        if not self.timers['tool use'].active and not self.timers['seed use'].active and not self.sleep:
            self.direction.y = 0
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
                
            self.direction.x = 0
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
                
        # tool use
        if keys[pygame.K_SPACE]:
            self.frame_index = 0
            self.timers['tool use'].activate()
            self.direction = pygame.math.Vector2()
        
        # tool switch
        if keys[pygame.K_q] and not self.timers['tool switch'].active and not self.timers['tool use'].active:
            self.tool_index += 1
            if self.tool_index >= len(self.tools):
                self.tool_index = 0
            self.selected_tool = self.tools[self.tool_index]
            self.timers['tool switch'].activate()
        
        # seed use
        if keys[pygame.K_LCTRL]:
            self.frame_index = 0
            self.timers['seed use'].activate()
            self.direction = pygame.math.Vector2()
        
        # seed switch
        if keys[pygame.K_e] and not self.timers['seed switch'].active and not self.timers['seed use'].active:
            self.seed_index += 1
            if self.seed_index >= len(self.seeds):
                self.seed_index = 0
            self.selected_seed = self.seeds[self.seed_index]
            self.timers['seed switch'].activate()
        
        # interaction
        if keys[pygame.K_RETURN] and not self.timers['toggle shop'].active:
            interaction_sprite = pygame.sprite.spritecollide(self, self.interactors, False)
            if interaction_sprite:
                if interaction_sprite[0].name == 'Bed':
                    self.status = 'left_idle'
                    self.sleep = True
                elif interaction_sprite[0].name == 'Trader':
                    self.timers['toggle shop'].activate()
                    self.toggle_shop()
        
        if keys[pygame.K_y]:
            self.soil.water_all()

# (self > update)
    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

# (self > update)
    def move(self, dt):
        # normalize direction
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.collisions('horizontal')
        self.rect.centerx = self.hitbox.centerx

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.collisions('vertical')
        self.rect.centery = self.hitbox.centery

# (self > move)
    def collisions(self, direction):
        for sprite in self.colliders.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0: # moving right
                            self.hitbox.right = sprite.hitbox.left
                        elif self.direction.x < 0: # moving left
                            self.hitbox.left = sprite.hitbox.right
                    elif direction == 'vertical':
                        if self.direction.y > 0: # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        elif self.direction.y < 0: # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                    self.pos.x = self.hitbox.centerx
                    self.pos.y = self.hitbox.centery

# (self > update)
    def get_target_pos(self):
        self.target_pos = self.pos + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

# (self > input > Timer > update)
    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil.get_hit_tile(self.target_pos)
        elif self.selected_tool == 'axe':
            for tree in self.trees.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
        elif self.selected_tool == 'water':
            self.soil.water(self.target_pos)

# (self > input > Timer > update)
    def use_seed(self):
        if self.inventory[f'{self.selected_seed} seed']:
            if self.soil.plant_seed(self.target_pos, self.selected_seed):
                self.inventory[f'{self.selected_seed} seed'] -= 1

# (self > update)
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

# (self > update)
    def get_cursor(self):
        mouse_pos = pygame.mouse.get_pos()
        self.soil.get_hovered_tile(mouse_pos, self.pos)

# (level > run)
    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_cursor()

        self.move(dt)
        self.get_target_pos()
        self.animate(dt) # animate with given status    
