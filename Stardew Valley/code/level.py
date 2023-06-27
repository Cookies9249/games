import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import *
from support import *
from timer_class import Timer
from soil import SoilLayer
from pytmx.util_pygame import load_pygame
from sky import Rain, Sky
from random import randint
from menu import Menu

class Level:
    def __init__(self):
        # surface
        self.surface = pygame.display.get_surface()

        # sprite groups
        self.sprites = CameraGroup()
        self.colliders = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.interactors = pygame.sprite.Group()
        self.soil_layer = SoilLayer(self.sprites, self.colliders)

        # sky
        self.rain = Rain(self.sprites)
        self.raining = False
        self.soil_layer.raining = self.raining
        self.sky = Sky()
        
        # setup
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

        # shop
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False

        # music
        self.success = pygame.mixer.Sound('audio/success.wav')
        self.success.set_volume(0.3)
        self.music = pygame.mixer.Sound('audio/bg.wav')
        self.music.set_volume(0.2)
        self.music.play(loops = -1)

    # run on start (self > init)
    def setup(self):
        tmx_data = load_pygame('data/map.tmx')
        self.import_sprites(tmx_data)

        # trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(
                groups = [self.sprites, self.colliders, self.trees],
                surf = obj.image,
                pos = (obj.x, obj.y),
                tree_size = obj.name,
                update_inventory = self.update_inventory)

        # collision tiles
        for x, y, _ in tmx_data.get_layer_by_name('Collision').tiles():
            Generic(
                groups = self.colliders,
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE)),
                pos = (x * TILE_SIZE, y * TILE_SIZE))
        
        # player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    group = self.sprites, 
                    pos = (obj.x,obj.y), 
                    colliders = self.colliders,
                    trees = self.trees,
                    interactors = self.interactors,
                    soil = self.soil_layer,
                    toggle_shop = self.toggle_shop)
                
            if obj.name == 'Bed':
                Interactor(
                    groups = self.interactors,
                    size = (obj.width, obj.height),
                    pos = (obj.x, obj.y),
                    name = obj.name)

            if obj.name == 'Trader':
                Interactor(
                    groups = self.interactors,
                    size = (obj.width, obj.height),
                    pos = (obj.x, obj.y),
                    name = obj.name)
        
        # ground
        Generic(
            groups=self.sprites,
            surf=pygame.image.load('graphics/world/ground.png').convert_alpha(),
            pos=(0,0),
            layer_order=LAYERS['ground'])

    # import some sprites (self > setup)
    def import_sprites(self, tmx_data):
        # house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    groups=self.sprites, 
                    surf=surf, 
                    pos=(x * TILE_SIZE, y * TILE_SIZE), 
                    layer_order=LAYERS['house bottom'])
        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    groups=self.sprites, 
                    surf=surf, 
                    pos=(x * TILE_SIZE, y * TILE_SIZE)) # layer_order=LAYERS['main'] (default)
        
        # fences
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Fence(
                groups=[self.sprites, self.colliders], 
                surf=surf, 
                pos=(x * TILE_SIZE, y * TILE_SIZE))
        
        # water
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water(
                groups=self.sprites,
                pos=(x * TILE_SIZE, y * TILE_SIZE))
            
        # wildflowers (not on tiles) - sunflowers, blue flowers, bushes, mushrooms
        for obj in tmx_data.get_layer_by_name('Decoration'):
            Wildflower(
                groups=[self.sprites, self.colliders],
                surf=obj.image,
                pos=(obj.x, obj.y))

    # reset after new day (self > run > support > Transition > play)
    def reset(self):
        # update trees
        for tree in self.trees.sprites():
            if tree.tree_alive:
                for apple in tree.apples.sprites():
                    apple.kill()
                tree.create_fruit()
        
        # update plants
        self.soil_layer.update_plants()
        
        # update soil layers
        for soil_sprite in self.soil_layer.soil_sprites.sprites():
            tile_x = soil_sprite.rect.x // TILE_SIZE
            tile_y = soil_sprite.rect.y // TILE_SIZE
            tile = self.soil_layer.grid[tile_y][tile_x]
            if 'watered' not in tile and 'planted' not in tile:
                self.soil_layer.grid[tile_y][tile_x].remove('tilled')
        self.soil_layer.create_soil_tile()

        self.soil_layer.remove_water()
        self.raining = randint(0,10) > 7
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()
        
        # update sky
        self.sky.reset()

    # check for collisions with harvestable plants (self > run)
    def plant_collisions(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.update_inventory(plant.plant_type, 1)

                    # update grid
                    row = plant.rect.centery // TILE_SIZE
                    col = plant.rect.centerx // TILE_SIZE
                    if 'planted' in self.soil_layer.grid[row][col]:
                        self.soil_layer.grid[row][col].remove('planted')

                    # create particle
                    Particle(
                        groups=self.sprites,
                        surf=plant.image,
                        pos=plant.rect.topleft,
                        layer_order=LAYERS['fruit'],
                        duration=200)
                    plant.kill()

    # run every frame (main > run)      
    def run(self, dt):
        # display
        self.surface.fill('black')
        self.sprites.custom_draw(self.player)

        # sprites
        if self.shop_active:
            self.menu.update()
        else:
            self.sprites.update(dt)
            self.plant_collisions()

        # overlay
        self.overlay.display()

        # daytime
        self.sky.display(dt)

        # rain
        if self.raining and not self.shop_active:
            self.rain.update()
        
        # transition (new day)
        if self.player.sleep:
            self.transition.play()

        set_debug(f'all: {self.sprites} trees: {self.trees} soil: {self.soil_layer.soil_sprites} water: {self.soil_layer.water_sprites}')
        update_debug()

    # update inventory (self > plant_collisions) (sprites > Tree > damage)
    def update_inventory(self, item, count):
        self.player.inventory[item] += count
        self.success.play()

    # toggle the shop (player > input)
    def toggle_shop(self):
        self.shop_active = not self.shop_active

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
    
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        # ground
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.layer_order == layer:
                    offset_rect = sprite.rect.copy()  # camera
                    offset_rect.center -= self.offset
                    
                    # if sprite == player:
                    #     pygame.draw.rect(self.surface, 'red', offset_rect, 5)
                    #     hitbox_rect = sprite.hitbox.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.surface, 'green', hitbox_rect, 5)
                    #     target_pos = hitbox_rect.center + PLAYER_TOOL_OFFSET[sprite.status.split('_')[0]]
                    #     pygame.draw.circle(self.surface, 'blue', target_pos, 5)

                    if str(sprite.__class__) == "<class 'sprites.Generic'>" and sprite.name == 'cursor':
                        pygame.draw.rect(self.surface, 'darkgrey', offset_rect, 5)
                        sprite.kill()
                    else:
                        self.surface.blit(sprite.image, offset_rect)

