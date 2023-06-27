import pygame, sys 

SCREEN_SIZE = 600

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface((20,20)) 
		self.image.fill('red')
		self.rect = self.image.get_rect(center = (SCREEN_SIZE/2,SCREEN_SIZE/2))
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		if pygame.mouse.get_pos():
			self.rect.center = pygame.mouse.get_pos()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('assets/alpha.png').convert_alpha()
		self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
		self.rect = self.image.get_rect(center = (SCREEN_SIZE/2,SCREEN_SIZE/2))
		self.mask = pygame.mask.from_surface(self.image)
			
# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
clock = pygame.time.Clock()

# group setup
player = pygame.sprite.GroupSingle(Player())
obstacle = pygame.sprite.GroupSingle(Obstacle())

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill('white')
	
	# updating and drawing 
	player.update()
	obstacle.draw(screen)
	player.draw(screen)

	# collision
	if pygame.sprite.spritecollide(player.sprite, obstacle, False):
		if pygame.sprite.spritecollide(player.sprite, obstacle, False, pygame.sprite.collide_mask):
			player.sprite.image.fill('lime')
		else:
			player.sprite.image.fill('red')
	else:
		player.sprite.image.fill('red')
	
	pygame.display.update()
	clock.tick(60)