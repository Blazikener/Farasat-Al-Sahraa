import pygame
from settings import *

class UI:
	def __init__(self):
		# general setup
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
		self.title_font = pygame.font.Font(UI_FONT, 32)

		# Bar setup
		self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

		# Load assets
		self.weapon_graphics = [pygame.image.load(w['graphic']).convert_alpha() for w in weapon_data.values()]
		self.magic_graphics = [pygame.image.load(m['graphic']).convert_alpha() for m in magic_data.values()]

	def show_bar(self, current, max_amount, bg_rect, color):
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
		ratio = current / max_amount
		current_rect = bg_rect.copy()
		current_rect.width = bg_rect.width * ratio
		pygame.draw.rect(self.display_surface, color, current_rect)
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

	def show_knowledge_book(self, knowledge):
		"""Draws the Codex (Knowledge Base) with progress bars."""
		# Overlay
		overlay = pygame.Surface((WIDTH, HEIGTH))
		overlay.set_alpha(200)
		overlay.fill('#1a100a')
		self.display_surface.blit(overlay, (0,0))

		# Book panel
		book_rect = pygame.Rect(WIDTH//4, HEIGTH//8, WIDTH//2, HEIGTH*0.75)
		pygame.draw.rect(self.display_surface, '#3d2b1f', book_rect)
		pygame.draw.rect(self.display_surface, 'gold', book_rect, 5)

		# Title
		title_surf = self.title_font.render("CODEX OF FARASAT", False, 'gold')
		self.display_surface.blit(title_surf, title_surf.get_rect(midtop = (WIDTH//2, book_rect.top + 30)))

		# Knowledge Stats with Progress Bars
		y = book_rect.top + 100
		total_k = 0
		bar_width = book_rect.width - 100
		bar_height = 25
		bar_x = book_rect.left + 50
		
		for category, value in knowledge.items():
			total_k += value
			
			# Category name
			text = f"{category.upper()}: {int(value)}%"
			self.display_surface.blit(self.font.render(text, False, 'white'), (bar_x, y))
			y += 30
			
			# Progress bar background
			bar_rect = pygame.Rect(bar_x, y, bar_width, bar_height)
			pygame.draw.rect(self.display_surface, UI_BG_COLOR, bar_rect)
			
			# Progress bar fill
			progress_rect = bar_rect.copy()
			progress_rect.width = bar_width * (value / 100)
			# Color based on category
			if category == 'terrain':
				bar_color = '#8B4513'  # Brown for terrain
			elif category == 'wildlife':
				bar_color = '#228B22'  # Green for wildlife
			else:  # survival
				bar_color = '#FFD700'  # Gold for survival
			pygame.draw.rect(self.display_surface, bar_color, progress_rect)
			pygame.draw.rect(self.display_surface, 'white', bar_rect, 2)
			
			y += 50

		# Total Knowledge
		avg_k = total_k / 3
		total_text = f"TOTAL KNOWLEDGE: {int(avg_k)}%"
		total_surf = self.font.render(total_text, False, 'gold')
		self.display_surface.blit(total_surf, total_surf.get_rect(center = (WIDTH//2, y + 20)))
		
		# Total progress bar
		total_bar_rect = pygame.Rect(bar_x, y + 50, bar_width, bar_height + 5)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, total_bar_rect)
		total_progress_rect = total_bar_rect.copy()
		total_progress_rect.width = bar_width * (avg_k / 100)
		pygame.draw.rect(self.display_surface, 'gold', total_progress_rect)
		pygame.draw.rect(self.display_surface, 'gold', total_bar_rect, 3)

		# Progression Hints
		y = book_rect.bottom - 100
		if avg_k < UNLOCK_REQUIREMENTS['mangrove']:
			hint = f"Unlock Mangrove Forest: {int(avg_k)}% / {UNLOCK_REQUIREMENTS['mangrove']}%"
		elif avg_k < UNLOCK_REQUIREMENTS['winter']:
			hint = f"Unlock Winter Desert: {int(avg_k)}% / {UNLOCK_REQUIREMENTS['winter']}%"
		else:
			hint = "All Zones Unlocked - Journey to the Peak!"
		
		hint_surf = self.font.render(hint, False, 'gold')
		self.display_surface.blit(hint_surf, hint_surf.get_rect(center = (WIDTH//2, y)))
		
		# Close hint
		close_hint = pygame.font.Font(UI_FONT, 16).render("Press B to close", False, '#888888')
		self.display_surface.blit(close_hint, close_hint.get_rect(center = (WIDTH//2, book_rect.bottom - 40)))

	def weapon_overlay(self, weapon_index, knowledge_score, weapon_name):
		bg_rect = pygame.Rect(10, 630, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
		
		if knowledge_score >= WEAPON_UNLOCKS.get(weapon_name, 0):
			weapon_surf = self.weapon_graphics[weapon_index]
			self.display_surface.blit(weapon_surf, weapon_surf.get_rect(center = bg_rect.center))
		else:
			lock_surf = self.font.render("?", False, 'gray')
			self.display_surface.blit(lock_surf, lock_surf.get_rect(center = bg_rect.center))

		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
		# UI Hint: 'Q' for Weapon
		hint_surf = self.font.render("Q", False, 'gold')
		self.display_surface.blit(hint_surf, (bg_rect.left + 5, bg_rect.top + 5))

	def magic_overlay(self, magic_index):
		"""Display magic selection overlay with 'E' hint."""
		bg_rect = pygame.Rect(100, 630, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
		
		magic_surf = self.magic_graphics[magic_index]
		self.display_surface.blit(magic_surf, magic_surf.get_rect(center = bg_rect.center))
		
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
		# UI Hint: 'E' for Magic
		hint_surf = self.font.render("E", False, 'gold')
		self.display_surface.blit(hint_surf, (bg_rect.left + 5, bg_rect.top + 5))

	def codex_hint(self):
		"""Display 'B' hint for Codex in top-right corner."""
		hint_rect = pygame.Rect(WIDTH - 150, 10, 140, 30)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, hint_rect)
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, hint_rect, 2)
		
		hint_text = self.font.render("B - Codex", False, 'gold')
		self.display_surface.blit(hint_text, hint_text.get_rect(center = hint_rect.center))

	def display(self, player, total_knowledge):
		weapon_name = list(weapon_data.keys())[player.weapon_index]
		self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
		self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
		self.weapon_overlay(player.weapon_index, total_knowledge, weapon_name)
		self.magic_overlay(player.magic_index)
		self.codex_hint()