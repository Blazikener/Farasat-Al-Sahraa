import pygame
from settings import *
from math import sin

class UI:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
		self.title_font = pygame.font.Font(UI_FONT, 36)
		self.insight_font = pygame.font.Font(UI_FONT, 24)
		
		# Game Over specific font (larger)
		self.game_over_font = pygame.font.Font(UI_FONT, 60)
		
		self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

		self.weapon_graphics = []
		for weapon in weapon_data.values():
			path = weapon['graphic']
			self.weapon_graphics.append(pygame.image.load(path).convert_alpha())

		self.weapon_names = list(weapon_data.keys())

		self.magic_graphics = []
		for magic in magic_data.values():
			path = magic['graphic']
			self.magic_graphics.append(pygame.image.load(path).convert_alpha())
		
		# Load Shop Icon
		try:
			self.shop_icon_surf = pygame.image.load('../graphics/objects/shop_icon.png').convert_alpha()
			self.shop_icon_surf = pygame.transform.scale(self.shop_icon_surf, (40, 40))
		except Exception as e:
			self.shop_icon_surf = pygame.Surface((40, 40))
			self.shop_icon_surf.fill('gold')
			print(f"UI Error: {e}")

		# Insight Message System
		self.message = ""
		self.message_time = 0
		self.message_duration = 3000 
		self.transition_alpha = 255
		self.pulse_timer = 0

	def draw_parchment(self, rect):
		# Draw the background parchment style
		pygame.draw.rect(self.display_surface, '#d4b483', rect)
		pygame.draw.rect(self.display_surface, '#a68a56', rect, 8)
		pygame.draw.rect(self.display_surface, 'gold', rect.inflate(10, 10), 4)

	def trigger_insight(self, text):
		self.message = text
		self.message_time = pygame.time.get_ticks()

	def draw_insight_message(self):
		current_time = pygame.time.get_ticks()
		if self.message and current_time - self.message_time < self.message_duration:
			elapsed = current_time - self.message_time
			alpha = 255
			
			# Fade out in the last second
			if elapsed > 2000:
				alpha = 255 - int(((elapsed - 2000) / 1000) * 255)
			
			text_surf = self.insight_font.render(f"INSIGHT: {self.message}", False, 'gold')
			text_surf.set_alpha(alpha)
			text_rect = text_surf.get_rect(center = (WIDTH // 2, HEIGTH - 100))
			
			bg_surf = pygame.Surface((text_rect.width + 30, text_rect.height + 20), pygame.SRCALPHA)
			bg_surf.fill((0, 0, 0, int(alpha * 0.6)))
			
			self.display_surface.blit(bg_surf, text_rect.inflate(30, 20))
			self.display_surface.blit(text_surf, text_rect)

	def show_tutorial(self):
		overlay = pygame.Surface((WIDTH, HEIGTH))
		overlay.set_alpha(230)
		overlay.fill('#0a0a0a')
		self.display_surface.blit(overlay, (0,0))
		
		title = self.title_font.render("JOURNEY OF INSIGHT", False, 'gold')
		self.display_surface.blit(title, title.get_rect(center=(WIDTH//2, 100)))
		
		lines = [
			"ARROWS: Move through the shifting sands",
			"SPACE: Attack enemies or interpret objects",
			"L-CTRL: Cast ancient magic",
			"Q / E: Cycle weapons and abilities",
			"V: Open the Global Trader",
			"B: Read the Codex of Farasat",
			"---------------------------------------",
			"PROGRESSION: Gain Insight to open gated zones.",
			"Northwards the desert changes... if you have the vision.",
			"---------------------------------------",
			"PRESS ANY KEY TO WAKE UP"
		]
		
		y = 180
		for line in lines:
			color = 'gold' if "PROGRESSION" in line or "WAKE" in line else 'white'
			surf = self.font.render(line, False, color)
			self.display_surface.blit(surf, surf.get_rect(center = (WIDTH//2, y)))
			y += 40

	def show_shop(self, player, current_index):
		overlay = pygame.Surface((WIDTH, HEIGTH))
		overlay.set_alpha(210)
		overlay.fill('#1a100a')
		self.display_surface.blit(overlay, (0,0))
		
		shop_rect = pygame.Rect(WIDTH//4, HEIGTH//10, WIDTH//2, HEIGTH*0.8)
		self.draw_parchment(shop_rect)
		
		title_surf = self.title_font.render("THE DESERT TRADER", False, '#5c4033')
		title_rect = title_surf.get_rect(midtop = (WIDTH//2, shop_rect.top + 40))
		self.display_surface.blit(title_surf, title_rect)
		
		scraps_surf = self.font.render(f"AVAILABLE SCRAPS: {int(player.exp)}", False, '#8B4513')
		scraps_rect = scraps_surf.get_rect(midtop = (WIDTH//2, shop_rect.top + 90))
		self.display_surface.blit(scraps_surf, scraps_rect)

		for i, name in enumerate(self.weapon_names):
			if name == 'sword': continue 
			
			y_pos = shop_rect.top + 160 + (i-1) * 100
			item_rect = pygame.Rect(shop_rect.left + 50, y_pos, shop_rect.width - 100, 80)
			
			is_sel = i == current_index
			pygame.draw.rect(self.display_surface, '#c2a373' if is_sel else '#d4b483', item_rect)
			pygame.draw.rect(self.display_surface, 'gold' if is_sel else '#5c4033', item_rect, 3)
			
			icon = self.weapon_graphics[i]
			self.display_surface.blit(icon, icon.get_rect(midleft = (item_rect.left + 20, item_rect.centery)))
			
			if name in player.unlocked_weapons:
				status = "OWNED"
			else:
				status = f"COST: {weapon_data[name].get('cost', 150)}"
			
			self.display_surface.blit(self.font.render(name.upper(), False, '#3d2b1f'), (item_rect.left + 100, item_rect.top + 15))
			self.display_surface.blit(self.font.render(status, False, '#5c4033'), (item_rect.left + 100, item_rect.top + 45))

		footer_surf = self.font.render("ARROWS: Navigate | SPACE: Buy | V: Close", False, '#5c4033')
		self.display_surface.blit(footer_surf, footer_surf.get_rect(center = (WIDTH//2, shop_rect.bottom - 40)))

	def show_knowledge_book(self, knowledge):
		overlay = pygame.Surface((WIDTH, HEIGTH))
		overlay.set_alpha(210)
		overlay.fill('#1a100a')
		self.display_surface.blit(overlay, (0,0))
		
		book_rect = pygame.Rect(WIDTH//4, HEIGTH//10, WIDTH//2, HEIGTH*0.8)
		self.draw_parchment(book_rect)
		
		title_surf = self.title_font.render("CODEX OF FARASAT", False, '#5c4033')
		self.display_surface.blit(title_surf, title_surf.get_rect(midtop = (WIDTH//2, book_rect.top + 40)))
		
		y = book_rect.top + 130
		total_k = 0
		bar_width = book_rect.width - 160
		bar_x = book_rect.left + 80
		
		cats = {'terrain': '#8B4513', 'wildlife': '#228B22', 'survival': '#c2810a'}
		
		for key, color in cats.items():
			val = knowledge[key]
			total_k += val
			
			self.display_surface.blit(self.font.render(f"{key.upper()} INSIGHT: {int(val)}%", False, '#5c4033'), (bar_x, y))
			y += 35
			
			pygame.draw.rect(self.display_surface, '#3d2b1f', (bar_x, y, bar_width, 22))
			pygame.draw.rect(self.display_surface, color, (bar_x, y, bar_width * (val/100), 22))
			pygame.draw.rect(self.display_surface, '#5c4033', (bar_x, y, bar_width, 22), 2)
			y += 60
			
		avg_k = total_k / 3
		self.pulse_timer += 0.08
		pulse = 160 + (sin(self.pulse_timer) * 60)
		
		total_bar = pygame.Rect(bar_x - 20, y + 40, bar_width + 40, 35)
		pygame.draw.rect(self.display_surface, '#222222', total_bar)
		pygame.draw.rect(self.display_surface, (int(pulse), int(pulse*0.8), 0), (bar_x - 20, y + 40, (bar_width + 40) * (avg_k/100), 35))
		pygame.draw.rect(self.display_surface, 'gold', total_bar, 4)
		
		footer_surf = self.font.render("Press B to return", False, '#5c4033')
		self.display_surface.blit(footer_surf, footer_surf.get_rect(center = (WIDTH//2, book_rect.bottom - 40)))

	def show_popup(self, title, lines):
		overlay = pygame.Surface((WIDTH, HEIGTH))
		overlay.set_alpha(180)
		overlay.fill('#000000')
		self.display_surface.blit(overlay, (0,0))
		
		rect = pygame.Rect((WIDTH-750)//2, (HEIGTH-450)//2, 750, 450)
		self.draw_parchment(rect)
		
		title_surf = self.title_font.render(title, False, '#5c4033')
		self.display_surface.blit(title_surf, title_surf.get_rect(midtop = (WIDTH//2, rect.top + 30)))
		
		y = rect.top + 120
		for line in lines:
			surf = self.font.render(line, False, '#3d2b1f')
			self.display_surface.blit(surf, surf.get_rect(center = (WIDTH//2, y)))
			y += 45
			
		footer = self.font.render("Press RETURN to continue", False, '#5c4033')
		self.display_surface.blit(footer, footer.get_rect(center = (WIDTH//2, rect.bottom - 40)))

	def show_bar(self, current, max_amount, bg_rect, color):
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
		
		ratio = current / max_amount
		cur_rect = bg_rect.copy()
		cur_rect.width = bg_rect.width * ratio
		
		pygame.draw.rect(self.display_surface, color, cur_rect)
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

	def draw_transition(self):
		if self.transition_alpha > 0:
			overlay = pygame.Surface((WIDTH, HEIGTH))
			overlay.fill('black')
			overlay.set_alpha(self.transition_alpha)
			self.display_surface.blit(overlay, (0,0))
			self.transition_alpha -= 4

	def display(self, player):
		# Health and Energy
		self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
		self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
		
		# Weapon and Magic Slots
		slots = [(10, 'Q', player.weapon_index), (100, 'E', player.magic_index)]
		for x, key, idx in slots:
			rect = pygame.Rect(x, 630, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
			pygame.draw.rect(self.display_surface, UI_BG_COLOR, rect)
			
			surf = self.weapon_graphics[idx] if key == 'Q' else self.magic_graphics[idx]
			surf_rect = surf.get_rect(center = rect.center)
			self.display_surface.blit(surf, surf_rect)
			
			pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, rect, 3)
			self.display_surface.blit(self.font.render(key, False, 'gold'), (rect.right - 22, rect.bottom - 22))
		
		# Scraps HUD
		scraps_text_surf = self.font.render(f"SCRAPS: {int(player.exp)}", False, 'white')
		box_width = max(200, scraps_text_surf.get_width() + 60)
		icon_rect = pygame.Rect(WIDTH - box_width - 20, 10, box_width, 50)
		
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, icon_rect)
		pygame.draw.rect(self.display_surface, 'gold', icon_rect, 2)
		self.display_surface.blit(self.shop_icon_surf, (icon_rect.left + 5, icon_rect.top + 5))
		
		text_rect = scraps_text_surf.get_rect(midleft = (icon_rect.left + 50, icon_rect.centery))
		self.display_surface.blit(scraps_text_surf, text_rect)

		self.draw_insight_message()
		self.draw_transition()

	# --- NEW GAME OVER SCREEN ---
	def show_game_over(self):
		# 1. Dark Red/Black Overlay
		overlay = pygame.Surface((WIDTH, HEIGTH))
		overlay.set_alpha(200)
		overlay.fill((40, 5, 5)) # Deep red/black color
		self.display_surface.blit(overlay, (0,0))

		# 2. Main "LOST" Text with Shadow
		title_text = "LOST TO THE SANDS"
		shadow_surf = self.game_over_font.render(title_text, True, 'black')
		text_surf = self.game_over_font.render(title_text, True, '#8b0000') # Blood red
		
		# Draw shadow offset
		center_x, center_y = WIDTH // 2, HEIGTH // 2
		self.display_surface.blit(shadow_surf, shadow_surf.get_rect(center = (center_x + 4, center_y - 46)))
		self.display_surface.blit(text_surf, text_surf.get_rect(center = (center_x, center_y - 50)))

		# 3. Pulsing "Restart" Text
		self.pulse_timer += 0.1
		alpha = abs(sin(self.pulse_timer)) * 255
		
		restart_surf = self.font.render("Press SPACE to Rise Again", True, 'gold')
		restart_surf.set_alpha(int(alpha))
		self.display_surface.blit(restart_surf, restart_surf.get_rect(center = (center_x, center_y + 50)))