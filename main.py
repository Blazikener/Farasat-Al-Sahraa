import pygame, sys
from math import sin
from settings import *
from level import Level

class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Mirage of the Sahraa')
		self.clock = pygame.time.Clock()

		# State Management
		self.game_active = False 
		self.level = Level()

		# Menu Logic
		self.menu_options = ['START', 'SETTINGS', 'QUIT']
		self.menu_index = 0
		self.show_settings = False
		self.music_on = True

		# UI Assets
		self.font = pygame.font.Font(UI_FONT, 30)
		self.title_font = pygame.font.Font(UI_FONT, 75) # Larger for the title
		
		try:
			self.bg_surf = pygame.image.load('../graphics/ui/bg_menu.png').convert_alpha()
		except:
			self.bg_surf = pygame.Surface((WIDTH,HEIGTH))
			self.bg_surf.fill('#1a1a1a')
		
		# Music
		try:
			self.main_sound = pygame.mixer.Sound('../audio/main.ogg')
			self.main_sound.set_volume(0.4)
			self.main_sound.play(loops = -1)
		except:
			print("Music file not found")

		# Selection Sound
		try:
			self.select_sound = pygame.mixer.Sound('../audio/hit.wav')
			self.select_sound.set_volume(0.2)
			self.start_sound = pygame.mixer.Sound('../audio/start.wav')
		except:
			self.select_sound = None
			self.start_sound = None

	def draw_glowing_text(self, text, font, color, glow_color, center_pos):
		"""Creates a professional glowing outline effect."""
		# 1. Create the pulsing scale for the glow
		tick = pygame.time.get_ticks()
		# The glow expands and contracts over time
		glow_spread = 2 + int((sin(tick / 300) + 1) * 3) 
		
		# 2. Render the 'Glow' layer by drawing offsets in a circle
		for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
			glow_surf = font.render(text, False, glow_color)
			# Draw the glow layer multiple times with the spread offset
			glow_rect = glow_surf.get_rect(center = (center_pos[0] + dx * glow_spread, center_pos[1] + dy * glow_spread))
			self.screen.blit(glow_surf, glow_rect)

		# 3. Render the main text on top
		main_surf = font.render(text, False, color)
		main_rect = main_surf.get_rect(center = center_pos)
		self.screen.blit(main_surf, main_rect)

	def display_menu(self):
		"""Draws the interactive menu with the glowing title."""
		# Draw Background
		self.screen.blit(self.bg_surf, (0,0))
		
		# Draw Pulsing Glowing Title
		# Using 'Mirage of the Sahraa' as the suggested name
		self.draw_glowing_text("MIRAGE OF SAHRAA", self.title_font, 'gold', '#ffcc00', (WIDTH // 2, HEIGTH // 3))

		# Display Options
		if not self.show_settings:
			for index, option in enumerate(self.menu_options):
				if index == self.menu_index:
					tick = pygame.time.get_ticks()
					val = 150 + (sin(tick / 200) * 105)
					color = (val, val, 0) # Pulsing Yellow for selection
					prefix = "> " 
				else:
					color = TEXT_COLOR
					prefix = "  "

				option_surf = self.font.render(f"{prefix}{option}", False, color)
				option_rect = option_surf.get_rect(center = (WIDTH // 2, (HEIGTH // 2 + 50) + (index * 70)))
				self.screen.blit(option_surf, option_rect)
		else:
			# Settings Sub-menu
			status = "ON" if self.music_on else "OFF"
			self.draw_glowing_text(f"MUSIC: {status}", self.font, 'gold', '#664400', (WIDTH // 2, HEIGTH // 2))
			
			back_surf = self.font.render("Press ESC to Go Back", False, TEXT_COLOR)
			self.screen.blit(back_surf, back_surf.get_rect(center = (WIDTH // 2, HEIGTH // 2 + 100)))

	def handle_menu_input(self, event):
		if not self.show_settings:
			if event.key == pygame.K_UP:
				self.menu_index = (self.menu_index - 1) % len(self.menu_options)
				if self.select_sound: self.select_sound.play()
			
			elif event.key == pygame.K_DOWN:
				self.menu_index = (self.menu_index + 1) % len(self.menu_options)
				if self.select_sound: self.select_sound.play()

			elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
				selection = self.menu_options[self.menu_index]
				if selection == 'START':
					self.game_active = True
					if self.start_sound: self.start_sound.play()
				elif selection == 'SETTINGS':
					self.show_settings = True
				elif selection == 'QUIT':
					pygame.quit()
					sys.exit()
		else:
			if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN):
				self.music_on = not self.music_on
				if self.music_on: pygame.mixer.unpause()
				else: pygame.mixer.pause()
			if event.key == pygame.K_ESCAPE:
				self.show_settings = False

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				
				if not self.game_active:
					if event.type == pygame.KEYDOWN:
						self.handle_menu_input(event)
				else:
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_m:
							self.level.toggle_menu()

			if self.game_active:
				self.screen.fill(WATER_COLOR)
				self.level.run()
			else:
				self.display_menu()

			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()