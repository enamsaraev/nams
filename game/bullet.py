from abc import ABCMeta, abstractmethod
import pygame, pyganim, enemy


WIDTH = 11
HEIGHT = 7

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


ANIMATION_FIRE = [('plim/bullet.png')]


class Bullet(metaclass=ABCMeta):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.speed = 0
		self.x = x
		self.y = y

		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image.set_colorkey(pygame.Color(WHITE))

		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)
		
		self.maxlen = 0
		self.speed = 0

	def intersection_w_blocks(self, blocks):
		for b in blocks:
			if pygame.sprite.collide_rect(self, b):
				self.kill()

	def update(self):
		pass

	def death(self):
		self.kill()	



class Pbullet(pygame.sprite.Sprite, Bullet):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)

		self.speed = 4
		self.x = x
		self.y = y + 7

		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image.set_colorkey(pygame.Color(WHITE))

		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)
		
		self.maxlen = 300
		self.speed = 6
		self.direction = direction

		boltAnim = []
		for i in ANIMATION_FIRE:
			boltAnim.append((i, 0.1))
		self.boltAnimFire = pyganim.PygAnimation(boltAnim)
		self.boltAnimFire.play()

	def update(self, power, blocks):
		self.target_speed(power)

		self.image.fill(pygame.Color(WHITE))
		self.boltAnimFire.blit(self.image, (0, 0))

		self.maxlen -= 6
		if self.maxlen != 0:
			self.rect.x += (self.speed * self.direction)
			self.intersection_w_blocks(blocks)
		if self.maxlen == 0:
			self.death()

	def target_speed(self, power):
		if power and power.return_item():
			self.speed = 10


class Ebullet(pygame.sprite.Sprite, Bullet):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)

		self.speed = 2
		self.x = x
		self.y = y + 12

		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image.set_colorkey(pygame.Color(WHITE))

		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)
		self.direction = direction
		
		self.maxlen = 300

		boltAnim = []
		for i in ANIMATION_FIRE:
			boltAnim.append((i, 0.1))
		self.boltAnimFire = pyganim.PygAnimation(boltAnim)
		self.boltAnimFire.play()

	def update(self, blocks):
		self.image.fill(pygame.Color(WHITE))
		self.boltAnimFire.blit(self.image, (0, 0))
		self.move_x = self.speed
		self.rect.x += (self.speed * self.direction)
		self.intersection_w_blocks(blocks)
		self.maxlen -= 6
		if self.maxlen == 0:
			self.death()

	def target_speed(self, enemy):
		for e in enemy:
			if e.return_right():
				self.speed = 6
			elif e.return_left():
				self.speed = -6


# class Grenade(pygame.sprite.Sprite):
# 	pygame.sprite.Sprite.__init__(self, x, y, direction)

# 		self.x = x
# 		self.y = y

# 		self.move_x = 7
# 		self.move_y = -11

# 		self.image = pygame.Surface((WIDTH, HEIGHT))
# 		self.image.set_colorkey(pygame.Color(WHITE))

# 		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)
		
# 		self.maxlen = 150
# 		self.speed = 0

# 		boltAnim = []
# 		for i in ANIMATION_FIRE:
# 			boltAnim.append((i, 0.1))
# 		self.boltAnimFire = pyganim.PygAnimation(boltAnim)
# 		self.boltAnimFire.play()

# 	def update(self):

# 		self.image.fill(pygame.Color(WHITE))
# 		self.boltAnimFire.blit(self.image, (0, 0))

# 		self.maxlen -= 6
# 		if self.maxlen != 0:
# 			self.rect.x += (self.speed * self.direction)
# 		else:
			







