import pygame, sys
from settings import *
from level import Level

# BUGS:
# - rain doesnt fill all unwatered tiles
# - lag with large amount of tiles
# - animation when sleeping
# - can sleep anytime
# - tree hitboxes
# - axe can hit stumps

# FUTURE UPDATES:
# - tree respawning
# - time
# - remove tiles without plant


class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('Sprout Land')
		self.clock = pygame.time.Clock()
		self.level = Level()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
  
			dt = self.clock.tick() / 1000
			self.level.run(dt)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
