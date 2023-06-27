import pygame
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

class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False
    
    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.active and current_time - self.start_time >= self.duration:
            self.deactivate()
            if self.func:
                self.func()