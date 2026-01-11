import pygame 
from settings import *
from tile import Tile, Mirage, CloudBarrier, TreasureChest, Key
from player import Player
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

class Level:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.game_paused = False
		self.show_codex = False

		# Sprite Groups
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()
		self.treasure_sprites = pygame.sprite.Group() 
		self.key_sprites = pygame.sprite.Group()

		self.animation_player = AnimationPlayer()
		self.ui = UI()
		
		self.create_map()
		self.upgrade = Upgrade(self.player)
		self.magic_player = MagicPlayer(self.animation_player)

		# Progress & Gating
		self.map_height = len(import_csv_layout('../map/map_Floor.csv')) * TILESIZE
		self.furthest_y = self.player.rect.centery
		self.cloud_group = pygame.sprite.Group()
		
		# Barriers
		self.mangrove_cloud = CloudBarrier(ZONE_THRESHOLDS['mangrove'], 500, [self.visible_sprites, self.obstacle_sprites, self.cloud_group], 'mangrove')
		self.winter_cloud = CloudBarrier(ZONE_THRESHOLDS['winter'], 800, [self.visible_sprites, self.obstacle_sprites, self.cloud_group], 'winter')

		# Key system
		self.player_has_key = False 

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map_Grass.csv'),
			'object': import_csv_layout('../map/map_Objects.csv'),
			'entities': import_csv_layout('../map/map_Entities.csv')
		}
		graphics = {
			'grass': import_folder('../graphics/Grass'),
			'objects': import_folder('../graphics/objects'),
			'mirage': pygame.image.load('../graphics/mirage/oasis.png').convert_alpha(),
			'chest_closed': pygame.image.load('../graphics/objects/chest_closed.png').convert_alpha(),
			'chest_open': pygame.image.load('../graphics/objects/chest_open.png').convert_alpha(),
			'key': pygame.image.load('../graphics/objects/key.png').convert_alpha()
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],'grass',random_grass_image)
						if style == 'object':
							# Check specific IDs FIRST to avoid IndexError
							if col == '21': 
								Mirage((x,y),[self.visible_sprites],graphics['mirage'])
							elif col == '99': 
								TreasureChest((x,y), [self.visible_sprites, self.obstacle_sprites, self.treasure_sprites], graphics['chest_closed'], graphics['chest_open'])
							elif col == '100':
								Key((x,y), [self.visible_sprites, self.key_sprites], graphics['key'])
							else:
								# Only try to index graphics['objects'] if it's within range
								obj_index = int(col)
								if obj_index < len(graphics['objects']):
									surf = graphics['objects'][obj_index]
									Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)
						if style == 'entities':
							if col == '394':
								self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack,self.create_magic)
							else:
								monster_name = 'bamboo' if col == '390' else 'spirit' if col == '391' else 'raccoon' if col == '392' else 'squid'
								Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.damage_player,self.trigger_death_particles,self.add_exp,self.animation_player)

	def interaction_logic(self):
		"""Handles key collection and chest interaction."""
		# 1. Key Collection
		for key_sprite in self.key_sprites:
			if key_sprite.hitbox.colliderect(self.player.hitbox):
				key_sprite.kill()
				self.player_has_key = True

		# 2. Chest Interaction
		keys_pressed = pygame.key.get_pressed()
		for sprite in self.treasure_sprites:
			if sprite.hitbox.colliderect(self.player.hitbox.inflate(20,20)):
				if keys_pressed[pygame.K_SPACE]:
					if self.player_has_key:
						if sprite.open_chest():
							# Unlock all knowledge categories
							self.player.knowledge['terrain'] = 100
							self.player.knowledge['survival'] = 100
							self.player.knowledge['wildlife'] = 100
					else:
						# Print to console for now; you could add a UI popup
						print("The chest is locked. You need a key!")

	def create_attack(self):
		self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

	def create_magic(self,style,strength,cost):
		if style == 'heal':
			self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
		if style == 'flame':
			self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])

	def destroy_attack(self):
		if self.current_attack: self.current_attack.kill()
		self.current_attack = None

	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							pos = target_sprite.rect.center
							offset = pygame.math.Vector2(0,75)
							for leaf in range(randint(3,6)):
								self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
							target_sprite.kill()
						else:
							if hasattr(target_sprite, 'get_damage'):
								target_sprite.get_damage(self.player,attack_sprite.sprite_type)

	def study_enemy_logic(self):
		for sprite in self.attackable_sprites:
			if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy' and not sprite.is_studied:
				dist = sprite.get_player_distance_direction(self.player)[0]
				if dist < sprite.notice_radius and not self.player.attacking:
					sprite.study_progress += 0.5
					if sprite.study_progress >= sprite.study_target:
						sprite.is_studied = True
						self.player.knowledge['survival'] = min(100, self.player.knowledge['survival'] + 5)

	def update_terrain_knowledge(self):
		current_y = self.player.rect.centery
		if current_y < self.furthest_y:
			self.furthest_y = current_y
			total_dist = self.map_height - current_y
			percentage = min(100, (total_dist / self.map_height) * 100)
			if percentage > self.player.knowledge['terrain']:
				self.player.knowledge['terrain'] = int(percentage)

	def damage_player(self,amount,attack_type):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

	def trigger_death_particles(self,pos,particle_type):
		self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

	def add_exp(self,amount):
		self.player.knowledge['wildlife'] = min(100, self.player.knowledge['wildlife'] + (amount / 100))

	def toggle_menu(self):
		self.game_paused = not self.game_paused 

	def toggle_codex(self):
		self.show_codex = not self.show_codex

	def gating_logic(self, total_k):
		if total_k >= UNLOCK_REQUIREMENTS['mangrove'] and self.mangrove_cloud.alive():
			self.mangrove_cloud.kill()
		if total_k >= UNLOCK_REQUIREMENTS['winter'] and self.winter_cloud.alive():
			self.winter_cloud.kill()

	def run(self):
		total_knowledge = sum(self.player.knowledge.values()) / len(self.player.knowledge)
		self.visible_sprites.custom_draw(self.player)
		
		if not self.game_paused and not self.show_codex:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.player_attack_logic()
			self.study_enemy_logic()
			self.update_terrain_knowledge()
			self.interaction_logic() # Key pickup and Chest check
			self.gating_logic(total_knowledge)

		self.ui.display(self.player, total_knowledge)
		
		if self.game_paused:
			self.upgrade.display()
		elif self.show_codex:
			self.ui.show_knowledge_book(self.player.knowledge)

		for sprite in self.visible_sprites:
			if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'mirage':
				sprite.update_visibility(self.player)

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()
		self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)                     
			               






























































