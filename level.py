import pygame 
from settings import *
from tile import Tile, Mirage, CloudBarrier, TreasureChest, Key, DroppedWeapon
from player import Player
from support import *
from random import choice, randint, random
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

class Level:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.game_paused = False; self.show_codex = False; self.shop_active = False
		self.shop_index = 1; self.active_popup = None

		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()
		self.treasure_sprites = pygame.sprite.Group() 
		self.key_sprites = pygame.sprite.Group()
		self.dropped_weapon_sprites = pygame.sprite.Group()

		self.animation_player = AnimationPlayer(); self.ui = UI()
		self.create_map()
		self.upgrade = Upgrade(self.player) 
		self.magic_player = MagicPlayer(self.animation_player)
		self.map_height = len(import_csv_layout('../map/map_Floor.csv')) * TILESIZE
		self.furthest_y = self.player.rect.centery
		
		self.mangrove_cloud = CloudBarrier(ZONE_THRESHOLDS['mangrove'], 500, [self.visible_sprites, self.obstacle_sprites], 'mangrove')
		self.winter_cloud = CloudBarrier(ZONE_THRESHOLDS['winter'], 800, [self.visible_sprites, self.obstacle_sprites], 'winter')
		self.player_has_key = False 

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map_Grass.csv'),
			'object': import_csv_layout('../map/map_Objects.csv'),
			'entities': import_csv_layout('../map/map_Entities.csv')
		}
		self.weapon_graphics = {name: pygame.image.load(data['graphic']).convert_alpha() for name, data in weapon_data.items()}
		graphics = {
			'grass': import_folder('../graphics/Grass'), 'objects': import_folder('../graphics/objects'),
			'mirage': pygame.image.load('../graphics/mirage/oasis.png').convert_alpha(),
			'chest_closed': pygame.image.load('../graphics/objects/chest_closed.png').convert_alpha(),
			'chest_open': pygame.image.load('../graphics/objects/chest_open.png').convert_alpha(),
			'key': pygame.image.load('../graphics/objects/key.png').convert_alpha()
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x, y = col_index * TILESIZE, row_index * TILESIZE
						if style == 'boundary': Tile((x,y),[self.obstacle_sprites],'invisible')
						if style == 'grass': Tile((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],'grass',choice(graphics['grass']))
						if style == 'object':
							if col == '21': Mirage((x,y),[self.visible_sprites],graphics['mirage'])
							elif col == '99': TreasureChest((x,y), [self.visible_sprites, self.obstacle_sprites, self.treasure_sprites], graphics['chest_closed'], graphics['chest_open'], 'lance')
							elif col == '100': Key((x,y), [self.visible_sprites, self.key_sprites], graphics['key'])
							else:
								idx = int(col)
								if idx < len(graphics['objects']): Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',graphics['objects'][idx])
						if style == 'entities':
							if col == '394': self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack,self.create_magic)
							else:
								if random() < 0.4:
									m_name = 'bamboo' if col == '390' else 'spirit' if col == '391' else 'ringtail' if col == '392' else 'squid'
									Enemy(m_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.damage_player,self.trigger_death_particles,self.add_exp,self.animation_player)

	def interaction_logic(self):
		for key in self.key_sprites:
			if key.hitbox.colliderect(self.player.hitbox): key.kill(); self.player_has_key = True; self.ui.trigger_insight("Obtained key.")
		for dw in self.dropped_weapon_sprites:
			if dw.hitbox.colliderect(self.player.hitbox.inflate(10,10)): self.player.add_weapon(dw.weapon_name); dw.kill(); self.ui.trigger_insight(f"Learned {dw.weapon_name.upper()}.")
		keys = pygame.key.get_pressed()
		for ch in self.treasure_sprites:
			if ch.hitbox.colliderect(self.player.hitbox.inflate(30,30)) and keys[pygame.K_SPACE]:
				if self.player_has_key and ch.open_chest():
					self.visible_sprites.shake(12); DroppedWeapon(ch.rect.center, [self.visible_sprites, self.dropped_weapon_sprites], ch.weapon_contents, self.weapon_graphics[ch.weapon_contents])
					self.player.knowledge = {k: 100 for k in self.player.knowledge}; self.ui.trigger_insight("Farasat increases.")

	def gating_logic(self, total_k):
		if total_k >= UNLOCK_REQUIREMENTS['mangrove'] and self.mangrove_cloud.alive(): self.mangrove_cloud.kill(); self.ui.trigger_insight("Mangrove gates open.")
		if total_k >= UNLOCK_REQUIREMENTS['winter'] and self.winter_cloud.alive(): self.winter_cloud.kill(); self.ui.trigger_insight("Winter gates open.")

	def damage_player(self,amount,attack_type):
		if self.player.vulnerable:
			self.visible_sprites.shake(18); self.player.health -= amount; self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks(); self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass': target_sprite.kill()
						else:
							if hasattr(target_sprite, 'get_damage'): target_sprite.get_damage(self.player, attack_sprite.sprite_type)

	def run(self):
		tk = sum(self.player.knowledge.values()) / 3
		self.visible_sprites.custom_draw(self.player)
		if not self.game_paused and not self.show_codex and not self.active_popup and not self.shop_active:
			self.visible_sprites.update(); self.visible_sprites.enemy_update(self.player); self.interaction_logic(); self.player_attack_logic(); self.gating_logic(tk)
			curr_y = self.player.rect.centery
			if curr_y < self.furthest_y: self.furthest_y = curr_y; self.player.knowledge['terrain'] = int(min(100, ((self.map_height - curr_y) / self.map_height) * 100))
		
		self.ui.display(self.player)
		if self.game_paused: self.upgrade.display()
		elif self.show_codex: self.ui.show_knowledge_book(self.player.knowledge)
		elif self.shop_active: self.ui.show_shop(self.player, self.shop_index)
		elif self.active_popup: self.ui.show_popup(self.active_popup[0], self.active_popup[1])
		for s in self.visible_sprites:
			if hasattr(s, 'sprite_type') and s.sprite_type == 'mirage': s.update_visibility(self.player)

	def create_attack(self): self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])
	def destroy_attack(self): 
		if hasattr(self, 'current_attack') and self.current_attack: self.current_attack.kill(); self.current_attack = None
	def create_magic(self,style,strength,cost):
		if style == 'heal': self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
		if style == 'flame': self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])
	def trigger_death_particles(self,pos,p_type): self.animation_player.create_particles(p_type,pos,self.visible_sprites)
	def add_exp(self,amount): self.player.knowledge['wildlife'] = min(100, self.player.knowledge['wildlife'] + (amount / 100)); self.player.exp += amount
	def toggle_menu(self): self.game_paused = not self.game_paused 
	def toggle_codex(self): self.show_codex = not self.show_codex

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__(); self.display_surface = pygame.display.get_surface(); self.half_width = WIDTH // 2; self.half_height = HEIGTH // 2; self.offset = pygame.math.Vector2()
		self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert(); self.floor_rect = self.floor_surf.get_rect(topleft = (0,0)); self.shake_amount = 0
	def shake(self, intensity): self.shake_amount = intensity
	def custom_draw(self,player):
		self.offset.x = player.rect.centerx - self.half_width; self.offset.y = player.rect.centery - self.half_height
		if self.shake_amount > 0: self.offset.x += randint(-self.shake_amount, self.shake_amount); self.offset.y += randint(-self.shake_amount, self.shake_amount); self.shake_amount -= 1
		self.display_surface.blit(self.floor_surf, self.floor_rect.topleft - self.offset)
		for s in sorted(self.sprites(),key = lambda s: s.rect.centery): self.display_surface.blit(s.image, s.rect.topleft - self.offset)
	def enemy_update(self,player):
		for e in [s for s in self.sprites() if hasattr(s,'sprite_type') and s.sprite_type == 'enemy']: e.enemy_update(player)