import pygame
from os import walk, listdir
from settings import *
from timer_class import Timer

pygame.init()

font = pygame.font.Font(None,30)
debug_message = ''
def set_debug(info):
    global debug_message
    debug_message = info

def update_debug():
    global debug_message
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(debug_message), True, 'white')
    debug_rect = debug_surf.get_rect(topleft = (10,10))
    display_surface.blit(debug_surf, debug_rect)

def import_folder(folder_path):
    surf_list = []
    for _, _, img_files in walk(folder_path):
        for img in img_files:
            surf = pygame.image.load(folder_path + '/' + img)
            surf_list.append(surf)
    return surf_list

def import_folder_dict(folder_path):
    surf_dict = {}
    for _, _, img_files in walk(folder_path):
        for img in img_files:
            file_name = img.split('.')[0]
            surf = pygame.image.load(folder_path + '/' + img)
            surf_dict[file_name] = surf
    return surf_dict

class Transition:
    def __init__(self, reset, player):
        # setup
        self.surface = pygame.display.get_surface()
        self.reset = reset
        self.player = player
        # overlay image
        self.image = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.color = 255
        self.speed = -0.5
    
    def play(self):
        self.color += self.speed
        if self.color <= 0:
            self.color = 0
            self.speed = 0.75
            self.reset()
        if self.color > 255:
            self.color = 255
            self.speed = -0.5
            self.player.sleep = False
        self.image.fill((self.color, self.color, self.color))
        self.surface.blit(self.image, (0,0), special_flags=pygame.BLEND_RGBA_MULT)