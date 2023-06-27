import pygame, sys
from random import randint
from helper import *

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
INV_WIDTH = 9
INV_HEIGHT = 2

pygame.init()
font = pygame.font.Font(None,30)

items = [{'id':0, 'name': None,     'img':None, 'stack':None},
         {'id':1, 'name':'red',     'img':None, 'stack':16},
	     {'id':2, 'name':'orange',  'img':None, 'stack':16},
         {'id':3, 'name':'yellow',  'img':None, 'stack':16},
         {'id':4, 'name':'green',   'img':None, 'stack':16},
         {'id':5, 'name':'blue',    'img':None, 'stack':16},
         {'id':6, 'name':'purple',  'img':None, 'stack':16},
         {'id':7, 'name':'white',   'img':None, 'stack':16},
         {'id':8, 'name':'brown',   'img':None, 'stack':16}]

inventory = [[{'item_id':None, 'sprite':None, 'count':0} for _ in range(INV_WIDTH)] for _ in range(INV_HEIGHT)]

class Inventory:
    def __init__(self) -> None:
        # general
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Inventory')
        self.clock = pygame.time.Clock()
        self.slot_sprites = InventoryGroup()

        # inventory
        self.init_inventory()
        self.fill_inventory()

        # selected slot
        self.click = False

    # initialize inventory bg (self > init)
    def init_inventory(self):
        self.spacing = 20
        self.size = 64
        self.width = len(inventory[0]) * (self.size + self.spacing) + self.spacing
        self.height = len(inventory) * (self.size + self.spacing) + self.spacing
        centerx = SCREEN_WIDTH // 2
        centery = SCREEN_HEIGHT // 2
        self.inventory_surf = pygame.Surface((self.width, self.height))
        self.inventory_surf.fill('grey')
        self.inventory_rect = self.inventory_surf.get_rect(center = (centerx, centery))

    # fill inventory with sprites (self > init)
    def fill_inventory(self):
        # temp fill items
        for i in range(2):
            for j in range(len(items) - 1):
                inventory[i][j]['item_id'] = j + 1
                inventory[i][j]['count'] = randint(1, 16)

        # create sprites
        for c in range(INV_HEIGHT):
            for r in range(INV_WIDTH):
                slot = inventory[c][r]
                slot['sprite'] = Slot(
                    groups = self.slot_sprites,
                    item = slot['item_id'],
                    count = slot['count'],
                    posx = r * (self.size + self.spacing) + self.spacing + self.inventory_rect.left,
                    posy = c * (self.size + self.spacing) + self.spacing + self.inventory_rect.top,
                    size = self.size
                )
        self.selected_sprite = Mouse(groups=self.slot_sprites, size=self.size)

    # (self > update)
    def input(self):
        keys = pygame.key.get_pressed()

        if event.type == pygame.MOUSEBUTTONDOWN and not self.click:
            mouse_pos = pygame.mouse.get_pos()
            self.mouse_button_down(mouse_pos)
            self.click = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.click = False
            
    # (self > input)
    def mouse_button_down(self, pos):
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            for c in range(INV_HEIGHT):
                for r in range(INV_WIDTH):
                    slot = inventory[c][r]
                    if slot['sprite'].rect.collidepoint(pos):
                        # get clicked item, add to selected item
                        self.check_swap((c, r))
        if mouse[2]:
            for c in range(INV_HEIGHT):
                for r in range(INV_WIDTH):
                    slot = inventory[c][r]
                    if slot['sprite'].rect.collidepoint(pos):
                        # get clicked item, add to selected item
                        self.check_split((c, r))

    # swap two inventory slots (self > mouse_button_down)
    def check_swap(self, pos):
        # swap pair info
        click = inventory[pos[0]][pos[1]] # clicked slot
        click_item = click['item_id']
        click_count = click['count']
        sel = self.selected_sprite # item selected by mouse
        sel_item = sel.item_id
        sel_count = sel.count

        if not click_item: # if clicked slot is empty
            # drop selected item
            click['item_id'] = sel_item
            click['count'] = sel_count
            sel.drop()

        elif sel_item: # if holding item
            if sel_item != click_item: # if different items, swap
                # drop selected item
                click['item_id'] = sel_item
                click['count'] = sel_count

                # select clicked item
                sel.select(click_item, click_count)
            
            elif sel_item == click_item: # if same items, add
                # drop items, if possible
                click['count'] = min(sel_count + click_count, items[click['item_id']]['stack'])
                if click["count"] == sel_count + click_count: # if all items dropped
                    # drop selected item
                    sel.drop()
                else: # if not all items dropped
                    sel.select(sel_item, sel_count + click_count - click['count'])
                
        else: # if not holding item
            # select clicked item
            sel.select(click_item, click_count)
            click['item_id'] = None
            click['count'] = 0

    # split selected item into two (self > mouse_button_down)
    def check_split(self, pos):
        # swap pair info
        click = inventory[pos[0]][pos[1]] # clicked slot
        click_item = click['item_id']
        click_count = click['count']
        sel = self.selected_sprite # item selected by mouse
        sel_item = sel.item_id
        sel_count = sel.count
        
        if not click_item: # if clicked slot is empty
            # drop one of selected item
            click['item_id'] = sel_item
            click['count'] = 1
            sel.count = sel_count - 1

        elif sel_item: # if holding item            
            if sel_item == click_item: # if same items, add
                # drop items, if possible
                click['count'] = min(click_count + 1, items[click['item_id']]['stack'])
                if click["count"] == click_count + 1: # if all items dropped
                    sel.select(sel_item, sel_count - 1)
                    if not sel_count - 1:
                        sel.drop()
                
        else: # if not holding item
            # select half of clicked item
            sel.select(click_item, click_count // 2)
            click['count'] = click_count - click_count // 2

    # update sprites to match inventory list (self > update)
    def update_inventory(self):
        # current iterates through whole inventory list and updates each slot individually
        for c in range(INV_HEIGHT):
            for r in range(INV_WIDTH):
                slot = inventory[c][r]
                slot['sprite'].update_slot(item=slot['item_id'], count=slot['count'])
        self.selected_sprite.update()

    # update the entire inventory (init)
    def update(self):        
        # draw bg
        self.screen.fill('black')
        self.screen.blit(self.inventory_surf, self.inventory_rect)

        # update all slots
        self.update_inventory()
        self.input()

        # draw sprites
        self.slot_sprites.draw_sprites(self.screen)


class Slot(pygame.sprite.Sprite):
    # (Inventory > fill_inventory)
    def __init__(self, groups, item, count, posx, posy, size) -> None:
        super().__init__(groups)
        # general
        self.item_id = item
        self.count = count

        # sprite setup
        self.image = pygame.Surface((size, size))
        if self.item_id:
            self.image.fill(items[self.item_id]['name'])
        else:
            self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = (posx, posy))

    # update slot to match slot_dict (Inventory > update_inventory)
    def update_slot(self, item, count):
        # update variables
        self.item_id = item

        if not self.item_id:
            count = 0
        self.count = count

        if self.item_id:
            self.image.fill(items[self.item_id]['name'])
        else:
            self.image.fill('grey')


class Mouse(pygame.sprite.Sprite):
    # (Inventory > fill_inventory)
    def __init__(self, groups, size) -> None:
        super().__init__(groups)
        # general
        self.item_id = None
        self.count = None
        self.image = None
        self.rect = None
        self.size = int(size)

    # update slot to match slot_dict (Inventory > mouse_button_down)
    def select(self, item, count):
        self.item_id = item
        self.count = count
        
        if item and count:
            pos = pygame.mouse.get_pos()
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(items[self.item_id]['name'])
            self.rect = self.image.get_rect(center = pos)            
    
    def drop(self):
        self.item_id = None
        self.count = 0
        self.image = None
        self.rect = None

    # update to mouse position (Inventory > update_inventory)
    def update(self):
        pos = pygame.mouse.get_pos()
        if self.rect:
            self.rect.center = pos


class InventoryGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
    
    def draw_sprites(self, screen):
        for sprite in self.sprites():
            if str(sprite.__class__) == "<class '__main__.Slot'>":
                # draw item
                screen.blit(sprite.image, sprite.rect)

                # draw text (count)
                if sprite.count > 1:
                    text = font.render(str(sprite.count), False, 'black')
                    rect = text.get_rect(bottomright = sprite.rect.bottomright)
                    screen.blit(text, rect)
            elif str(sprite.__class__) == "<class '__main__.Mouse'>":
                # draw item
                if sprite.image and sprite.rect:
                    screen.blit(sprite.image, sprite.rect)

                    # draw text (count)
                    if sprite.count > 1:
                        text = font.render(str(sprite.count), False, 'black')
                        rect = text.get_rect(bottomright = sprite.rect.bottomright)
                        screen.blit(text, rect)


inventory_class = Inventory()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    inventory_class.update()
    update_debug()
    pygame.display.update()