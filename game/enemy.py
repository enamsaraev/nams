from abc import ABCMeta, abstractmethod
import pygame
import pyganim, bullet

enemies = pygame.sprite.Group()
enemy_bl = pygame.sprite.Group()

D_WIDTH = 23
D_HEIGHT = 25

B_WIDTH = 31
B_HEIGHT = 40

WHITE = (255, 255, 255)

MOVE = 1

ANIMATION_DELAY = 0.1

ANIMATION_RIGHT = [
	('plim/enemy-1.png'),
	('plim/enemy-2.png'),
	('plim/enemy-3.png')
]
ANIMATION_LEFT = [
	('plim/enemy-4.png'),
	('plim/enemy-5.png'),
	('plim/enemy-6.png')
]
ANIMATION_DEATH = [('plim/death.png', 0.1)]

B_ANIMATION_RIGHT = [
	('plim/boss-1.png'),
	('plim/boss-2.png'),
	('plim/boss-3.png')
]
B_ANIMATION_LEFT = [
	('plim/boss-4.png'),
	('plim/boss-5.png'),
	('plim/boss-6.png')
]


class Enemy(metaclass=ABCMeta):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.x = x
		self.y = y

		self.move_x = 0
		self.maxLen = 0
		self.health = 0
		self.c = 0

		
		self.direction = 0


	def update(self):
		pass

	def go_right(self):
		self.image.fill(pygame.Color(WHITE))
		self.boltAnimRight.blit(self.image, (0, 0))
		self.move_x = MOVE
		self.direction = 1

	def go_left(self):
		self.image.fill(pygame.Color(WHITE))
		self.boltAnimLeft.blit(self.image, (0, 0))
		self.move_x = -MOVE
		self.direction = -1

	def intersection_w_blocks(self, blocks):
		for b in blocks:
			if pygame.sprite.collide_rect(self, b):
				self.move_x = 0

	def is_dead(self, bullets):
		for b in bullets:
			if pygame.sprite.collide_rect(self, b):
				self.health -= 1
				b.death()
	
	def shoot(self):
		self.c += 1
		if self.c == 30:
			e_bl = bullet.Ebullet(self.rect.x, self.rect.y, self.direction)
			enemy_bl.add(e_bl)
			self.c = 0

	def return_direction(self):
		return self.direction


class Default_enemy(pygame.sprite.Sprite, Enemy):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.x = x
		self.y = y + 5

		self.move_x = 0
		self.maxLen = 50
		self.health = 2
		self.c = 0

		self.direction = 0

		self.image = pygame.Surface((D_WIDTH, D_HEIGHT))
		self.image.set_colorkey(pygame.Color(WHITE))

		self.rect = pygame.Rect(self.x, self.y, D_WIDTH, D_HEIGHT)

		boltAnim = []
		for i in ANIMATION_RIGHT:
			boltAnim.append((i, ANIMATION_DELAY))
		self.boltAnimRight = pyganim.PygAnimation(boltAnim)
		self.boltAnimRight.play()

		boltAnim = []
		for i in ANIMATION_LEFT:
			boltAnim.append((i, ANIMATION_DELAY))
		self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
		self.boltAnimLeft.play()

		self.boltAnimDeath = pyganim.PygAnimation(ANIMATION_DEATH)
		self.boltAnimDeath.play()

		self.image.fill(pygame.Color(WHITE))
		self.boltAnimLeft.blit(self.image, (0, 0))

	def update(self, player, bullets, blocks):
		if self.health > 0:
			player_rect_x = player.return_rectx()
			player_rect_y = player.return_recty()

			if abs(self.rect.y - player_rect_y ) < 20 and abs(self.rect.x - player_rect_x) <= 100:

				self.shoot()

				if (self.rect.x - player_rect_x) < 0:
					self.go_right()
				if (self.rect.x - player_rect_x) > 0:
					self.go_left()

				self.intersection_w_blocks(blocks)
			else:
				self.move_x = 0

			self.is_dead(bullets)

		else:
			self.image.fill(pygame.Color(WHITE))
			self.boltAnimDeath.blit(self.image, (0, 0))
			self.move_x = 0
			# self.rect.y += 1

		self.rect.x += self.move_x

class Boss_enemy(pygame.sprite.Sprite, Enemy):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.x = x
		self.y = y - 7

		self.move_x = 0
		self.maxLen = 50
		self.health = 3
		self.c = 0

		self.left = False
		self.right = False

		self.image = pygame.Surface((B_WIDTH, B_HEIGHT))
		self.image.set_colorkey(pygame.Color(WHITE))

		self.rect = pygame.Rect(self.x, self.y, B_WIDTH, B_HEIGHT)

		boltAnim = []
		for i in B_ANIMATION_RIGHT:
			boltAnim.append((i, ANIMATION_DELAY))
		self.boltAnimRight = pyganim.PygAnimation(boltAnim)
		self.boltAnimRight.play()

		boltAnim = []
		for i in B_ANIMATION_LEFT:
			boltAnim.append((i, ANIMATION_DELAY))
		self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
		self.boltAnimLeft.play()

		self.boltAnimDeath = pyganim.PygAnimation(ANIMATION_DEATH)
		self.boltAnimDeath.play()

		self.image.fill(pygame.Color(WHITE))
		self.boltAnimRight.blit(self.image, (0, 0))

	def update(self, player, bullets, blocks):
		if self.health > 0:
			player_rect_x = player.return_rectx()
			player_rect_y = player.return_recty()

			if abs(self.rect.y - player_rect_y ) < 40 and abs(self.rect.x - player_rect_x) <= 100:

				self.shoot()

				if (self.rect.x - player_rect_x) < 0:
					self.go_right()
				if (self.rect.x - player_rect_x) > 0:
					self.go_left()

				self.intersection_w_blocks(blocks)
			else:
				self.move_x = 0

			self.is_dead(bullets)
			
		else:
			self.image.fill(pygame.Color(WHITE))
			self.boltAnimDeath.blit(self.image, (0, 0))
			self.move_x = 0
			# self.rect.y += 1

		self.rect.x += self.move_x







