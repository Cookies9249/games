import pygame
from settings import *
from support import *
from timer_class import Timer

class Menu:
    # (level > init)
    def __init__(self, player, toggle_menu) -> None:
        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

        # options
        self.menu_width = 400
        self.space = 10
        self.padding = 8

        # entries
        self.options = list(self.player.inventory.keys())
        self.sell_border = 3 #####################

        # movement
        self.index = 0
        self.timer = Timer(200)

        self.setup()
    
    # set up bg of shop (self > init)
    def setup(self):
        # create surfaces for text
        self.text_surf_list = []
        self.menu_height = 0
        for item in self.options:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surf_list.append(text_surf)
            self.menu_height += text_surf.get_height() + (self.padding * 2)

        # create rect for menu background
        self.menu_height += (len(self.text_surf_list) - 1) * self.space
        self.menu_top = (SCREEN_HEIGHT - self.menu_height) / 2
        self.menu_left = (SCREEN_WIDTH - self.menu_width) / 2
        self.menu_rect = pygame.Rect(self.menu_left, self.menu_top, self.menu_width, self.menu_height)

    # display player balance (self > update) 
    def display_money(self):
        surf = self.font.render(f'Balance: ${self.player.money}', False, 'black')
        rect = surf.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))
        pygame.draw.rect(self.surface, 'white', rect.inflate(15,10), 0, 6)  # bg for text
        self.surface.blit(surf, rect)

    # create display for each item entry (self > update)
    def display_entries(self):
        self.amount = list(self.player.inventory.values())

        for i, text_surf in enumerate(self.text_surf_list):
            # dimensions
            entry_height = text_surf.get_height() + self.padding * 2
            entry_top = self.menu_top + i * (entry_height + self.space)
            
            # background
            bg_rect = pygame.Rect(self.menu_left, entry_top, self.menu_width, entry_height)
            pygame.draw.rect(self.surface, 'white', bg_rect, 0, 4)
            
            # text
            text_rect = text_surf.get_rect(midleft = (self.menu_left + 20, bg_rect.centery))
            self.surface.blit(text_surf, text_rect)

            # amount
            amount_surf = self.font.render(str(self.amount[i]), False, 'black')
            amount_rect = amount_surf.get_rect(midright = (self.menu_rect.right - 20, bg_rect.centery))
            self.surface.blit(amount_surf, amount_rect)

            # if selected
            if self.index == i:
                pygame.draw.rect(self.surface, 'black', bg_rect, 4, 4)
                
                # buy / sell text
                current_item = self.options[self.index]
                if self.index <= self.sell_border:
                    price = SALE_PRICES[current_item]
                    self.sell_text = self.font.render(f'sell: ${price}', False, 'black')
                    pos_rect = self.sell_text.get_rect(midleft = (self.menu_rect.centerx, bg_rect.centery))
                    self.surface.blit(self.sell_text, pos_rect)
                else:
                    price = PURCHASE_PRICES[current_item]
                    self.buy_text = self.font.render(f'buy: ${price}', False, 'black')
                    pos_rect = self.buy_text.get_rect(midleft = (self.menu_rect.centerx, bg_rect.centery))
                    self.surface.blit(self.buy_text, pos_rect)

    # check input to control shop (self > update)
    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()
        self.player.timers['toggle shop'].update()

        if keys[pygame.K_ESCAPE] or keys[pygame.K_RETURN] and not self.player.timers['toggle shop'].active:
            self.toggle_menu()
            self.player.timers['toggle shop'].activate()
        
        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()
            elif keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()
            
            if keys[pygame.K_SPACE]:
                self.timer.activate()
                current_item = self.options[self.index]
                if self.index <= self.sell_border:  # sell
                    if self.player.inventory[current_item] > 0:
                        self.player.inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]
                
                else:  # buy
                    price = PURCHASE_PRICES[current_item]
                    if self.player.money >= price:
                        self.player.inventory[current_item] += 1
                        self.player.money -= price
        
        if self.index < 0:
            self.index = len(self.options) - 1
        elif self.index > len(self.options) - 1:
            self.index = 0
    
    # show the menu (level > run)
    def update(self):
        self.input()
        self.display_money()
        self.display_entries()

        
            
            


        