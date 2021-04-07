import pygame
from abc import ABCMeta


WIDTH = 32
HEIGHT = 32

GREEN = (0, 255, 0)


class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image = pygame.image.load('plim/ground.png')
		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)


class Block(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image = pygame.image.load('plim/dirt.png')
		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)


class Block_with_spikes(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image = pygame.image.load('plim/block_spikes.png')
		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)

class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image = pygame.image.load('plim/lava.png')
		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)









