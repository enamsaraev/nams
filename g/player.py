import pygame, time
import pyganim, platform, bullet, enemy, things
from os import path

pygame.init()

snd_dir = path.join(path.dirname(__file__), 'sounds')
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shoot.wav'))
walk_sound = pygame.mixer.Sound(path.join(snd_dir, 'step.wav'))

player_bl = pygame.sprite.Group()
player_grnd = pygame.sprite.Group()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH = 29
HEIGHT = 40

MOVE = 5
JUMP = 20
GRAV = 1

ANIMATION_DELAY = 0.1
ANIMATION_RIGHT = [
	('plim/player_r_run-1.png'),
	('plim/player_r_run-2.png'),
	('plim/player_r_run-3.png')
]
ANIMATION_LEFT = [
	('plim/player_l_run-1.png'),
	('plim/player_l_run-2.png'),
	('plim/player_l_run-3.png')
]
ANIMATION_JUMPFIRE_RIGHT = [('plim/player_r_run-2.png', 0.1)]
ANIMATION_JUMPFIRE_LEFT = [('plim/player_l_run-2.png', 0.1)]
ANIMATION_JUMP = [('plim/player_stay.png', 0.1)]
ANIMATION_STAY = [('plim/player_stay.png', 0.1)]

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.dead = False

		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)

		self.move_x = 0
		self.move_y = 0
		self.health = 10
		self.ground = False
		self.direction = 0

		self.image = pygame.Surface((WIDTH, HEIGHT))
		self.image.set_colorkey(pygame.Color(WHITE))
		self.image.fill(pygame.Color(WHITE))

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

		self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
		self.boltAnimStay.play()
		self.boltAnimStay.blit(self.image, (0, 0))

		self.boltAnimJFRight = pyganim.PygAnimation(ANIMATION_JUMPFIRE_RIGHT)
		self.boltAnimJFRight.play()

		self.boltAnimJFLeft = pyganim.PygAnimation(ANIMATION_JUMPFIRE_LEFT)
		self.boltAnimJFLeft.play()

		self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
		self.boltAnimJump.play()

	def update(self, left, right, jump, fire, blocks):
		if not left and not right:
			self.stay()
		if left:
			self.left()
		if right:
			self.right()
		if jump:
			self.jump()
		if fire:
			self.fire(left, right)

		if not self.ground:
			self.move_y += GRAV

		self.ground = False

		self.rect.y += self.move_y
		self.intersection_w_blocks(0, self.move_y, blocks)
		self.intersection_w_bullets(0, self.move_y, enemy.enemy_bl)

		self.rect.x += self.move_x
		self.intersection_w_blocks(self.move_x, 0, blocks)
		self.intersection_w_bullets(self.move_x, 0, enemy.enemy_bl)

	def shoot(self):
		p_bl = bullet.Pbullet(self.rect.x, self.rect.y, self.return_direction())
		player_bl.add(p_bl)
		shoot_sound.play()

	# def grenade(self):
	# 	grnd = bullet.Grenade(self.rect.x, self.rect.y, self.return_direction())
	# 	player_grnd.add(grnd)
	# 	# shoot_sound.play()

	def left(self):
		self.move_x = -MOVE
		self.image.fill(pygame.Color(WHITE))
		self.boltAnimLeft.blit(self.image, (0, 0))
		self.direction = -1

	def right(self):
		self.move_x = MOVE
		self.image.fill(pygame.Color(WHITE))
		self.boltAnimRight.blit(self.image, (0, 0))
		self.direction = 1

	def jump(self):
		if self.ground:
			self.move_y = -JUMP
		self.image.fill(pygame.Color(WHITE))
		self.boltAnimJump.blit(self.image, (0, 0))

	def stay(self):
		self.move_x = 0

	def fire(self, left, right):
		if left:
			self.image.fill(pygame.Color(WHITE))
			self.boltAnimJFLeft.blit(self.image, (0, 0))
		if right:
			self.image.fill(pygame.Color(WHITE))
			self.boltAnimJFRight.blit(self.image, (0, 0))

	def intersection_w_blocks(self, move_x, move_y, blocks):
		for b in blocks:
			if pygame.sprite.collide_rect(self, b):
				if move_x > 0:
					self.rect.right = b.rect.left
				if move_x < 0:
					self.rect.left = b.rect.right
				if move_y > 0:
					self.rect.bottom = b.rect.top
					self.ground = True
					self.move_y = 0
				if move_y < 0:
					self.rect.top = b.rect.bottom
					self.move_y = 0

				if isinstance(b, platform.Block_with_spikes) or isinstance(b, platform.Lava):
					self.health -= 5

	def intersection_w_bullets(self, move_x, move_y, e_bullets):
		for b in e_bullets:
			if pygame.sprite.collide_rect(self, b):
				b.death()
				self.health -= 2

	def draw_shield_bar(self, screen, x, y):
		for i in things.hp:
			if i.return_item():
				self.health = 10
		l = 100
		h = 10
		fill = (self.health / 10) * l
		fill_rect = pygame.Rect(x, y, fill, h)
		pygame.draw.rect(screen, GREEN, fill_rect)
		if self.health <= 0:
			self.death()
			self.dead = True

	def death(self):
		self.dead = True
		time.sleep(1)
		self.teleport(self.x, self.y)
 
	def teleport(self, toX, toY):
		self.rect.x = toX
		self.rect.y = toY

	def return_rectx(self):
		return self.rect.x

	def return_recty(self):
		return self.rect.y

	def return_direction(self):
		return self.direction

	def is_dead(self):
		return self.dead










