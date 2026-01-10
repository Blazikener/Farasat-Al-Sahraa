import pygame, sys
from math import sin
from settings import *
from level import Level

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Mirage of the Sahraa')
		self.clock = pygame.time.Clock()

		self.game_active = False 
		self.level = Level()

		# Menu Setup
		self.menu_options = ['START', 'SETTINGS', 'QUIT']
		self.menu_index = 0
		self.show_settings = False
		self.music_on = True

		self.font = pygame.font.Font(UI_FONT, 30)
		self.title_font = pygame.font.Font(UI_FONT, 75) 
		
		try:
			self.bg_surf = pygame.image.load('../graphics/ui/bg_menu.png').convert_alpha()
		except:
			self.bg_surf = pygame.Surface((WIDTH,HEIGTH))
			self.bg_surf.fill('#1a1a1a')
		
		try:
			self.main_sound = pygame.mixer.Sound('../audio/main.ogg')
			self.main_sound.set_volume(0.4)
			self.main_sound.play(loops = -1)
		except: pass

	def draw_glowing_text(self, text, font, color, glow_color, center_pos):
		tick = pygame.time.get_ticks()
		glow_spread = 2 + int((sin(tick / 300) + 1) * 3) 
		for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
			glow_surf = font.render(text, False, glow_color)
			glow_rect = glow_surf.get_rect(center = (center_pos[0] + dx * glow_spread, center_pos[1] + dy * glow_spread))
			self.screen.blit(glow_surf, glow_rect)
		main_surf = font.render(text, False, color)
		self.screen.blit(main_surf, main_surf.get_rect(center = center_pos))

	def display_menu(self):
		self.screen.blit(self.bg_surf, (0,0))
		self.draw_glowing_text("MIRAGE OF SAHRAA", self.title_font, 'gold', '#ffcc00', (WIDTH // 2, HEIGTH // 3))

		if not self.show_settings:
			for index, option in enumerate(self.menu_options):
				color = (255, 255, 0) if index == self.menu_index else TEXT_COLOR
				prefix = "> " if index == self.menu_index else "  "
				option_surf = self.font.render(f"{prefix}{option}", False, color)
				option_rect = option_surf.get_rect(center = (WIDTH // 2, (HEIGTH // 2 + 50) + (index * 70)))
				self.screen.blit(option_surf, option_rect)
		else:
			status = "ON" if self.music_on else "OFF"
			self.draw_glowing_text(f"MUSIC: {status}", self.font, 'gold', '#664400', (WIDTH // 2, HEIGTH // 2))
			back_surf = self.font.render("Press ESC to Go Back", False, TEXT_COLOR)
			self.screen.blit(back_surf, back_surf.get_rect(center = (WIDTH // 2, HEIGTH // 2 + 100)))

	def handle_menu_input(self, event):
		if not self.show_settings:
			if event.key == pygame.K_UP: self.menu_index = (self.menu_index - 1) % len(self.menu_options)
			elif event.key == pygame.K_DOWN: self.menu_index = (self.menu_index + 1) % len(self.menu_options)
			elif event.key == pygame.K_RETURN:
				selection = self.menu_options[self.menu_index]
				if selection == 'START': self.game_active = True
				elif selection == 'SETTINGS': self.show_settings = True
				elif selection == 'QUIT': pygame.quit(); sys.exit()
		else:
			if event.key == pygame.K_ESCAPE: self.show_settings = False

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: pygame.quit(); sys.exit()
				
				if not self.game_active:
					if event.type == pygame.KEYDOWN: self.handle_menu_input(event)
				else:
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE: self.level.toggle_menu()
						if event.key == pygame.K_b: self.level.toggle_codex()

			if self.game_active:
				self.screen.fill('#000000') 
				self.level.run()
			else:
				self.display_menu()

			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()