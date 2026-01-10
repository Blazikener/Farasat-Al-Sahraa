import pygame
import math
from settings import *
from random import randint, choice

class Treasure(pygame.sprite.Sprite):
	def __init__(self, pos, groups, treasure_type='common'):
		super().__init__(groups)
		self.sprite_type = 'treasure'
		self.treasure_type = treasure_type  # 'common', 'rare', 'legendary'
		
		# Create visual representation
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		if treasure_type == 'common':
			self.image.fill('#FFD700')  # Gold
		elif treasure_type == 'rare':
			self.image.fill('#C0C0C0')  # Silver
		else:  # legendary
			self.image.fill('#FF69B4')  # Pink/Magical
		
		# Draw treasure chest icon
		pygame.draw.rect(self.image, '#8B4513', (8, 8, 48, 48), 3)
		pygame.draw.circle(self.image, '#FFD700', (32, 20), 8)
		
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(-10, -10)
		
		# Treasure rewards
		self.rewards = {
			'common': {'knowledge': {'terrain': 2, 'wildlife': 1, 'survival': 1}, 'health': 10},
			'rare': {'knowledge': {'terrain': 5, 'wildlife': 3, 'survival': 3}, 'health': 25},
			'legendary': {'knowledge': {'terrain': 10, 'wildlife': 8, 'survival': 8}, 'health': 50}
		}
		
		self.collected = False
		self.glow_time = 0
		
	def update(self):
		# Pulsing glow effect
		self.glow_time += 1
		if not self.collected:
			alpha = int(200 + 55 * math.sin(self.glow_time * 0.1))
			self.image.set_alpha(min(255, alpha))
	
	def collect(self, player, knowledge_dict):
		"""Collect treasure and apply rewards."""
		if self.collected:
			return False
		
		self.collected = True
		rewards = self.rewards[self.treasure_type]
		
		# Apply knowledge rewards
		for category, amount in rewards['knowledge'].items():
			knowledge_dict[category] = min(100, knowledge_dict[category] + amount)
		
		# Apply health reward
		player.health = min(player.stats['health'], player.health + rewards['health'])
		
		return True

