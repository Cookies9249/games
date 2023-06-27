import pygame
from settings import *

class Overlay:
    def __init__(self, player):
        # general
        self.surface = pygame.display.get_surface()
        self.player = player

        # imports
        self.tools_surf = {tool: pygame.image.load(f'graphics/overlay/{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'graphics/overlay/{seed}.png').convert_alpha() for seed in player.seeds}
    
    def display(self):
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])

        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom = OVERLAY_POSITIONS['seed'])

        self.surface.blit(tool_surf, tool_rect)
        self.surface.blit(seed_surf, seed_rect)