import pygame 
from settings import *
from random import randint

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
	def __init__(self,pos,groups,closed_surf,open_surf,weapon_name = None):
		super().__init__(groups)
		self.sprite_type = 'treasure'
		self.image_closed = closed_surf
		self.image_open = open_surf
		self.weapon_contents = weapon_name 
		
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

class DroppedWeapon(pygame.sprite.Sprite):
	def __init__(self,pos,groups,weapon_name,surface):
		super().__init__(groups)
		self.sprite_type = 'dropped_weapon'
		self.weapon_name = weapon_name
		self.image = surface
		
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(pos)
		self.target_pos = pygame.math.Vector2(pos) + pygame.math.Vector2(randint(-40,40), randint(30,70))
		self.hitbox = self.rect.inflate(0,-10)

	def update(self):
		if (self.target_pos - self.pos).magnitude() > 2:
			direction = (self.target_pos - self.pos).normalize()
			self.pos += direction * 3
			self.rect.center = self.pos

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
		self.alpha = 255

	def update_visibility(self, player):
		# Calculate distance between player and the oasis
		p_vec = pygame.math.Vector2(player.rect.center)
		m_vec = pygame.math.Vector2(self.rect.center)
		distance = (p_vec - m_vec).magnitude()

		# FADING LOGIC: Keeps it as a mirage that disappears when close
		if distance < 400:
			# Gradually decrease alpha as the player gets closer
			alpha = max(0, min(255, (distance - 100) / 300 * 255))
			self.alpha = int(alpha)
		else:
			self.alpha = 255
		
		self.image.set_alpha(int(self.alpha))