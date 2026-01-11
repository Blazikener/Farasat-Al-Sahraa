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

class TreasureChest(pygame.sprite.Sprite):
	def __init__(self,pos,groups,closed_surf,open_surf):
		super().__init__(groups)
		self.sprite_type = 'treasure'
		self.image_closed = closed_surf
		self.image_open = open_surf
		
		self.image = self.image_closed
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-10)
		self.is_open = False

	def open_chest(self):
		if not self.is_open:
			self.image = self.image_open
			self.is_open = True
			return True 
		return False

class Key(pygame.sprite.Sprite):
	def __init__(self,pos,groups,surface):
		super().__init__(groups)
		self.sprite_type = 'key'
		self.image = surface
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-10)

class CloudBarrier(pygame.sprite.Sprite):
	def __init__(self, y_pos, height, groups, zone_name):
		super().__init__(groups)
		self.sprite_type = 'cloud'
		self.zone_name = zone_name
		
		try:
			raw_cloud = pygame.image.load('../graphics/ui/cloud.png').convert_alpha()
			self.cloud_surf = pygame.transform.scale(raw_cloud, (320, 180)) 
		except:
			self.cloud_surf = pygame.Surface((320, 180))
			self.cloud_surf.fill('white')
			self.cloud_surf.set_alpha(150)

		world_width = 5000 
		self.image = pygame.Surface((world_width, height), pygame.SRCALPHA)
		
		for x in range(0, world_width, 320):
			for y in range(0, height, 180):
				self.image.blit(self.cloud_surf, (x, y))
		
		self.rect = self.image.get_rect(topleft = (-500, y_pos))
		self.hitbox = self.rect.inflate(0, 0) 

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
		from math import sin
		p_vec = pygame.math.Vector2(player.rect.center)
		m_vec = pygame.math.Vector2(self.rect.center)
		distance = (p_vec - m_vec).magnitude()

		time = pygame.time.get_ticks() / 50
		shimmer_amount = sin(time) * (3 if distance > 300 else 1.5)
		self.rect.x = self.origin_x + shimmer_amount

		if distance < 400:
			alpha = max(0, min(255, (distance - 100) / 300 * 255))
			self.alpha = int(alpha)
		else:
			self.alpha = 255
		
		self.image.set_alpha(int(self.alpha))