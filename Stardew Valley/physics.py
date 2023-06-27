import pygame, sys

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
INV_WIDTH = 9
INV_HEIGHT = 2

pygame.init()
font = pygame.font.Font(None,30)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Inventory')
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.image.fill('white')
        self.pos = self.rect.center
        self.velocity = 0
        self.acceleration = -1

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.velocity = 100
    
    def update(self):
        self.velocity += self.acceleration
        self.pos += (self.velocity, self.velocity)

        if self.pos[1] >= 600:
            self.pos[1] = 600
            self.velocity = 0
        
        self.rect.center = int(self.pos[0]), int(self.pos[1])
        
        
        
        

player = Player()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    player.update()
    pygame.display.update()