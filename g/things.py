from abc import ABCMeta, abstractmethod
import pygame
import pyganim

hp = pygame.sprite.Group()

WIDTH = 12
HEIGHT = 18

WHITE = (255, 255, 255)

HP_ANIMATION_BEFORE = [('plim/chan.png', 0.1)]
HP_ANIMATION_AFTER = [('plim/health.png', 0.1)]

P_ANIMATION_BEFORE = [('plim/chan.png', 0.1)]
P_ANIMATION_AFTER = [('plim/bullet.png', 0.1)]

class Thing(metaclass=ABCMeta):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.x = x
		self.y = y
		self.health = True

		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image.set_colorkey(pygame.Color(WHITE))

		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)

	def update(self, bullets, player):
		pass

	def return_item(self):
		pass

class Hp(pygame.sprite.Sprite, Thing):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.x = x
		self.y = y
		self.health = True
		self.after = False

		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image.set_colorkey(pygame.Color(WHITE))

		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)

		self.boltAnimBefore = pyganim.PygAnimation(HP_ANIMATION_BEFORE)
		self.boltAnimBefore.play()

		self.boltAnimAfter = pyganim.PygAnimation(HP_ANIMATION_AFTER)
		self.boltAnimAfter.play()

		self.image.fill(pygame.Color(WHITE))
		self.boltAnimBefore.blit(self.image, (0, 0))

	def update(self, bullets, player):
		self.health = True
		for b in bullets:
			if pygame.sprite.collide_rect(self, b):
				b.death()
				self.image.fill(pygame.Color(WHITE))
				self.boltAnimAfter.blit(self.image, (0, 0))
				self.after = True
		if self.after:
			if pygame.sprite.collide_rect(self, player):
				self.rect.x = 0
				self.rect.y = 0
				self.health = False

	def return_item(self):
		if not self.health:
			return 10


class Power(pygame.sprite.Sprite, Thing):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.x = x
		self.y = y
		self.health = True
		self.after = False

		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image.set_colorkey(pygame.Color(WHITE))

		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)

		self.boltAnimBefore = pyganim.PygAnimation(P_ANIMATION_BEFORE)
		self.boltAnimBefore.play()

		self.boltAnimAfter = pyganim.PygAnimation(P_ANIMATION_AFTER)
		self.boltAnimAfter.play()

		self.image.fill(pygame.Color(WHITE))
		self.boltAnimBefore.blit(self.image, (0, 0))

	def update(self, bullets, player):
		for b in bullets:
			if pygame.sprite.collide_rect(self, b):
				b.death()
				self.image.fill(pygame.Color(WHITE))
				self.boltAnimAfter.blit(self.image, (0, 0))
				self.after = True
		if self.after:
			if pygame.sprite.collide_rect(self, player):
				self.health = False
				self.kill()

	def return_item(self):
		if not self.health:
			return 6


class Door(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image = pygame.image.load('plim/door.png')
		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)













