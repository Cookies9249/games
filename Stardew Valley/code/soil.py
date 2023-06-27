import pygame
from settings import *
from support import *
from timer_class import Timer
from pytmx.util_pygame import load_pygame
from random import choice
from sprites import Generic

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.layer_order = LAYERS['soil']

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, groups, pos) -> None:
        super().__init__(groups)
        self.surf_list = import_folder('graphics/soil_water')
        self.image = choice(self.surf_list)
        self.rect = self.image.get_rect(topleft = pos)
        self.layer_order = LAYERS['soil water']

class SoilLayer:
    def __init__(self, sprites, colliders) -> None:
        # sprite groups
        self.all_sprites = sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()
        self.colliders = colliders

        # graphics
        self.soil_surf_dict = import_folder_dict('graphics/soil_updated')

        self.create_soil_grid()
        self.create_soil_hitboxes()

        # sounds
        self.plant_sound = pygame.mixer.Sound('audio/plant.wav')
        self.plant_sound.set_volume(0.2)
        self.hoe_sound = pygame.mixer.Sound('audio/hoe.wav')
        self.hoe_sound.set_volume(0.4)
        self.water_sound = pygame.mixer.Sound('audio/water.wav')
        self.water_sound.set_volume(0.2)

    # create a 2D grid of farmable tiles (self > init)
    def create_soil_grid(self):
        ground = pygame.image.load('graphics/world/ground.png')
        h_tiles = ground.get_width() // int(TILE_SIZE)
        v_tiles = ground.get_height() // int(TILE_SIZE)
        
        self.grid = [[[] for _ in range(h_tiles)] for _ in range(v_tiles)]
        for x, y, _ in load_pygame('data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('farmable')

    # create a rect for every soil tile (self > init)
    def create_soil_hitboxes(self):
        self.hitboxes = []
        for row_index, row in enumerate(self.grid):
            for col_index, tile in enumerate(row):
                if 'farmable' in tile:
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hitboxes.append(rect)

    # detect which soil rect is hit (player > use_tool)
    def get_hit_tile(self, pos):
        for rect in self.hitboxes:
            if rect.collidepoint(pos):
                tile_x = rect.x // TILE_SIZE
                tile_y = rect.y // TILE_SIZE
                tile = self.grid[tile_y][tile_x]

                if 'farmable' and not 'tilled' in tile:
                    tile.append('tilled')
                    self.hoe_sound.play()
                    self.create_soil_tile()

                    if self.raining:
                        self.water_all()
    
    # create a soil patch (self > get_hit_tile)
    def create_soil_tile(self):
        for sprite in self.soil_sprites.sprites():
            sprite.kill()

        for row_index, row in enumerate(self.grid):
            for col_index, tile in enumerate(row):
                if 'tilled' in tile:
                    t = 'tilled' in self.grid[row_index - 1][col_index]
                    r = 'tilled' in row[col_index + 1]
                    b = 'tilled' in self.grid[row_index + 1][col_index]
                    l = 'tilled' in row[col_index - 1]

                    tile_type = ''
                    if t: tile_type += 't'
                    if r: tile_type += 'r'
                    if b: tile_type += 'b'
                    if l: tile_type += 'l'
                    if not tile_type: tile_type = 'o'

                    SoilTile(
                        groups = [self.all_sprites, self.soil_sprites],
                        surf = self.soil_surf_dict[tile_type],
                        pos = (col_index * TILE_SIZE, row_index * TILE_SIZE))
    
    # add water sprite on watered soil patches (player > use_tool)
    def water(self, pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(pos):
                tile_x = soil_sprite.rect.x // TILE_SIZE
                tile_y = soil_sprite.rect.y // TILE_SIZE
                tile = self.grid[tile_y][tile_x]
                if 'watered' not in tile:
                    tile.append('watered')
                    self.water_sound.play()

                    WaterTile(
                        groups = [self.all_sprites, self.water_sprites],
                        pos = soil_sprite.rect.topleft)
    
    # water all sprites when raining (level > reset), (self > get_hit_tile)
    def water_all(self):
        for row_index, row in enumerate(self.grid):
            for col_index, tile in enumerate(row):
                if 'tilled' in tile and not 'watered' in tile:
                    row[col_index].append('watered')
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    WaterTile(
                        groups = [self.all_sprites, self.water_sprites],
                        pos = (x,y))

    # remove water after new day + clean up grid (level > reset)
    def remove_water(self):
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        for row in self.grid:
            for tile in row:
                if 'watered' in tile:
                    tile.remove('watered')

    # show tile hovered by mouse (player > get_cursor)
    def get_hovered_tile(self, mouse_pos, player_pos):
        player_to_mouse = pygame.math.Vector2()
        offset_pos = pygame.math.Vector2()
        player_to_mouse.x = SCREEN_WIDTH / 2 - mouse_pos[0]
        player_to_mouse.y = SCREEN_HEIGHT / 2 - mouse_pos[1]

        offset_pos = player_pos - player_to_mouse

        if player_to_mouse.magnitude() >= 2 * TILE_SIZE:
            return

        for rect in self.hitboxes:
            if rect.collidepoint(offset_pos):
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                Generic(
                    groups = self.all_sprites, 
                    surf = surf, 
                    pos = rect.topleft, 
                    layer_order = LAYERS['main'] - 1, 
                    name = 'cursor')
                ##
                tile_x = rect.x // TILE_SIZE
                tile_y = rect.y // TILE_SIZE
    
    # update water status for plant (self > plant_seed)
    def check_watered(self, pos):
        tile_x = pos[0] // TILE_SIZE
        tile_y = pos[1] // TILE_SIZE
        tile = self.grid[tile_y][tile_x]
        
        return 'watered' in tile

    # plant a new crop on a tile (returns True if seed is planted)
    def plant_seed(self, target_pos, seed):
        for sprite in self.soil_sprites:
            if sprite.rect.collidepoint(target_pos):
                tile_x = sprite.rect.x // TILE_SIZE
                tile_y = sprite.rect.y // TILE_SIZE
                tile = self.grid[tile_y][tile_x]
                
                if 'planted' not in tile:
                    tile.append('planted')
                    self.plant_sound.play()
                    Plant(
                        groups = [self.all_sprites, self.plant_sprites, self.colliders],
                        soil_sprite = sprite,
                        plant_type = seed,
                        check_watered = self.check_watered)
                    return True
                return False

    # update plant growth (level > reset)
    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()

class Plant(pygame.sprite.Sprite):
    def __init__(self, groups, soil_sprite, plant_type, check_watered) -> None:
        super().__init__(groups)
        # general
        self.plant_type = plant_type
        self.soil_sprite = soil_sprite
        self.frames = import_folder(f'graphics/fruit/{plant_type}')
        self.layer_order = LAYERS['ground plant']
        self.check_watered = check_watered

        # growth
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        self.harvestable = False

        # sprite setup
        self.image = self.frames[self.age]
        self.offset = pygame.math.Vector2(0, -16 if plant_type == 'corn' else -8)
        self.rect = self.image.get_rect(midbottom = soil_sprite.rect.midbottom + self.offset)
        
    def grow(self):
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed

            if int(self.age) > 0:
                self.layer_order = LAYERS['main']
                self.hitbox = self.rect.copy().inflate(-26, -self.rect.height * 0.8)
                self.hitbox.bottom -= 20

            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True

            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom = self.soil_sprite.rect.midbottom + self.offset)

