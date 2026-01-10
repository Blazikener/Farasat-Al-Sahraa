import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)
		self.sprite_type = sprite_type
		# HITBOX_OFFSET is now correctly imported from settings
		y_offset = HITBOX_OFFSET[sprite_type]
		self.image = surface
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
		else:
			self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,y_offset)

class Mirage(pygame.sprite.Sprite):
	def __init__(self,pos,groups,surface):
		super().__init__(groups)
		self.sprite_type = 'mirage'
		self.image = surface.copy() 
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, -10)
		self.origin_x = self.rect.x 
		self.alpha = 255

	def update_visibility(self, player):
		"""Shimmer horizontally and fade as player approaches."""
		from math import sin
		p_vec = pygame.math.Vector2(player.rect.center)
		m_vec = pygame.math.Vector2(self.rect.center)
		distance = (p_vec - m_vec).magnitude()

		# Horizontal shimmer effect (vibration) - stronger when far away
		time = pygame.time.get_ticks() / 50
		shimmer_amount = sin(time) * (3 if distance > 300 else 1.5)
		self.rect.x = self.origin_x + shimmer_amount

		# Fade out as player approaches (acts as navigation trap)
		if distance < 400:
			# Fade starts at 400 pixels, fully faded at 100 pixels
			alpha = max(0, min(255, (distance - 100) / 300 * 255))
			self.alpha = int(alpha)
		else:
			self.alpha = 255
		
		self.image.set_alpha(int(self.alpha))