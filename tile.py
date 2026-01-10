import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)
		self.sprite_type = sprite_type
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
		# We create a copy to avoid modifying the original loaded image surface
		self.image = surface.copy() 
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, -10)
		self.origin_x = self.rect.x # Store original X for shimmering

	def update_visibility(self, player):
		"""Farasat Logic: Vanishes as you get closer to teach Environmental Interpretation."""
		p_vec = pygame.math.Vector2(player.rect.center)
		m_vec = pygame.math.Vector2(self.rect.center)
		distance = (p_vec - m_vec).magnitude()

		# SHIMMER: Make the oasis wobble slightly like a heat haze
		shimmer = (pygame.time.get_ticks() // 100) % 3
		self.rect.x = self.origin_x + (shimmer if distance > 300 else 0)

		# FADE: Mirage starts fading at 400 pixels and is gone by 100 pixels
		if distance < 400:
			alpha = (distance - 100) / 300 * 255
			self.alpha = max(0, min(255, alpha))
		else:
			self.alpha = 255
		
		self.image.set_alpha(int(self.alpha))