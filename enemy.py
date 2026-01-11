import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
	def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp,animation_player):

		# general setup
		super().__init__(groups)
		self.sprite_type = 'enemy'

		# graphics setup
		self.import_graphics(monster_name)
		self.status = 'idle'
		
		# SAFEGUARD: Check if animations were loaded to avoid IndexError
		if self.animations[self.status]:
			self.image = self.animations[self.status][self.frame_index]
		else:
			# Fallback if graphics are missing
			self.image = pygame.Surface((64,64))
			self.image.fill('red')

		# movement
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-10)
		self.obstacle_sprites = obstacle_sprites

		# stats
		self.monster_name = monster_name
		monster_info = monster_data[self.monster_name]
		self.health = monster_info['health']
		self.exp = monster_info['exp']
		self.speed = monster_info['speed']
		self.attack_damage = monster_info['damage']
		self.resistance = monster_info['resistance']
		self.attack_radius = monster_info['attack_radius']
		self.notice_radius = monster_info['notice_radius']
		self.attack_type = monster_info['attack_type']

		# player interaction
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
		self.damage_player = damage_player
		self.trigger_death_particles = trigger_death_particles
		self.add_exp = add_exp

		# Tracking & Farasat Logic
		self.animation_player = animation_player
		self.visible_sprites = groups[0] 
		self.last_track_frame = -1 
		self.study_progress = 0
		self.study_target = 100
		self.is_studied = False

		# invincibility timer
		self.vulnerable = True
		self.hit_time = None
		self.invincibility_duration = 300

		# sounds
		self.death_sound = pygame.mixer.Sound('../audio/death.wav')
		self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
		self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
		self.death_sound.set_volume(0.6)
		self.hit_sound.set_volume(0.6)
		self.attack_sound.set_volume(0.6)

	def import_graphics(self,name):
		self.animations = {'idle':[],'move':[],'attack':[]}
		main_path = f'../graphics/monsters/{name}/'
		for animation in self.animations.keys():
			self.animations[animation] = import_folder(main_path + animation)

	def get_player_distance_direction(self,player):
		enemy_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(player.rect.center)
		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance,direction)

	def get_status(self, player):
		distance = self.get_player_distance_direction(player)[0]

		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				self.frame_index = 0
			self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = 'move'
		else:
			self.status = 'idle'

	def actions(self,player):
		if self.status == 'attack':
			self.attack_time = pygame.time.get_ticks()
			self.damage_player(self.attack_damage,self.attack_type)
			self.attack_sound.play()
		elif self.status == 'move':
			self.direction = self.get_player_distance_direction(player)[1]
		else:
			self.direction = pygame.math.Vector2()

	def create_tracks(self):
		"""Realistic Tracking: Spawns footprints based on animation steps."""
		# Updated to check for 'ringtail' name
		if self.status == 'move' and self.monster_name in ['bamboo', 'ringtail']:
			current_frame = int(self.frame_index)
			
			if current_frame in [0, 2] and current_frame != self.last_track_frame:
				self.animation_player.create_particles(
					f'{self.monster_name}_track', 
					self.rect.midbottom, 
					[self.visible_sprites])
				self.last_track_frame = current_frame
			
			if current_frame not in [0, 2]:
				self.last_track_frame = -1

	def animate(self):
		animation = self.animations[self.status]
		
		# SAFEGUARD: Only animate if frames exist
		if not animation: return

		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True

		if not self.vulnerable:
			if current_time - self.hit_time >= self.invincibility_duration:
				self.vulnerable = True

	def get_damage(self,player,attack_type):
		if self.vulnerable:
			self.hit_sound.play()
			self.direction = self.get_player_distance_direction(player)[1]
			if attack_type == 'weapon':
				self.health -= player.get_full_weapon_damage()
			else:
				self.health -= player.get_full_magic_damage()
			self.hit_time = pygame.time.get_ticks()
			self.vulnerable = False

	def check_death(self):
		if self.health <= 0:
			self.kill()
			self.trigger_death_particles(self.rect.center,self.monster_name)
			self.add_exp(self.exp)
			self.death_sound.play()

	def hit_reaction(self):
		if not self.vulnerable:
			self.direction *= -self.resistance

	def update(self):
		self.hit_reaction()
		self.move(self.speed)
		self.animate()
		self.cooldowns()
		self.check_death()
		self.create_tracks()

	def enemy_update(self,player):
		self.get_status(player)
		self.actions(player)