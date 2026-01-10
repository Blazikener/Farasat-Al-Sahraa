import pygame, sys
from math import sin # Added standard math import for the breathing effect
from settings import *
from level import Level

class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Farasat Al Sahraa')
		self.clock = pygame.time.Clock()

		# State Management
		self.game_active = False # False = Show Menu, True = Play Game
		self.level = Level()

		# UI Assets - Using pixelated Joystix font from settings
		self.font = pygame.font.Font(UI_FONT, 30)
		self.title_font = pygame.font.Font(UI_FONT, 60)
		
		# Load images with error handling
		try:
			# Creating a Gold-colored pixelated Title
			self.title_surf = self.title_font.render('FARASAT AL SAHRAA', False, 'gold')
			self.bg_surf = pygame.image.load('../graphics/ui/bg_menu.png').convert_alpha()
		except:
			# Fallback if images aren't created yet or fail to load
			self.title_surf = self.title_font.render('FARASAT AL SAHRAA', False, 'white')
			self.bg_surf = pygame.Surface((WIDTH,HEIGTH))
			self.bg_surf.fill('#222222')
		
		# --- MUSIC LOGIC ---
		# Background music loops throughout the entire game session
		try:
			self.main_sound = pygame.mixer.Sound('../audio/main.ogg')
			self.main_sound.set_volume(0.5)
			self.main_sound.play(loops = -1) 
		except:
			print("Main music file missing at ../audio/main.ogg")

		try:
			self.start_sound = pygame.mixer.Sound('../audio/start.wav')
		except:
			self.start_sound = None

	def display_menu(self):
		"""Draws the Start Screen with a pixelated desert theme."""
		# Draw Background
		self.screen.blit(self.bg_surf, (0,0))
		
		# Draw Title
		title_rect = self.title_surf.get_rect(center = (WIDTH // 2, HEIGTH // 3))
		self.screen.blit(self.title_surf, title_rect)

		# Draw Instructions with a 'breathing' color effect for better feedback
		tick = pygame.time.get_ticks()
		# Corrected: Using sin from Python's math module
		color_val = 150 + (sin(tick / 200) * 105)
		
		text_surf = self.font.render('Press SPACE to Begin', False, (color_val, color_val, color_val))
		text_rect = text_surf.get_rect(center = (WIDTH // 2, HEIGTH // 2 + 100))
		
		self.screen.blit(text_surf, text_rect)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				
				if not self.game_active:
					if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
						self.game_active = True
						if self.start_sound:
							self.start_sound.play()
				else:
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_m:
							self.level.toggle_menu()

			if self.game_active:
				# Game loop
				self.screen.fill(WATER_COLOR)
				self.level.run()
			else:
				# Menu loop
				self.display_menu()

			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()