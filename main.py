import pygame, sys
from settings import *
from level import Level
from math import sin

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Farasat Al Sahraa')
        self.clock = pygame.time.Clock()

        self.game_active = False
        self.level = Level()
        
        # Menu Setup
        self.menu_options = ['START JOURNEY', 'QUIT']
        self.menu_index = 0
        self.show_tutorial = True
        
        # Fonts
        self.font = pygame.font.Font(UI_FONT, 30)
        self.title_font = pygame.font.Font(UI_FONT, 80)
        self.subtitle_font = pygame.font.Font(UI_FONT, 20)

        # Assets
        try:
            self.bg_surf = pygame.image.load('../graphics/ui/bg_menu.png').convert()
            self.bg_surf = pygame.transform.scale(self.bg_surf, (WIDTH, HEIGTH))
        except:
            # Create a beautiful desert gradient if image is missing
            self.bg_surf = pygame.Surface((WIDTH, HEIGTH))
            for y in range(HEIGTH):
                # Gradient from deep dusk orange to desert sand
                r = min(255, 40 + (y // 4))
                g = min(255, 20 + (y // 6))
                b = min(255, 10 + (y // 12))
                pygame.draw.line(self.bg_surf, (r, g, b), (0, y), (WIDTH, y))

        # Animation variables
        self.title_float = 0
        self.selection_glow = 0

    def draw_text_with_shadow(self, text, font, color, pos, shadow_color=(20, 10, 5)):
        # Shadow
        shadow_surf = font.render(text, False, shadow_color)
        self.screen.blit(shadow_surf, shadow_surf.get_rect(center=(pos[0] + 4, pos[1] + 4)))
        # Main text
        main_surf = font.render(text, False, color)
        self.screen.blit(main_surf, main_surf.get_rect(center=pos))

    def draw_menu(self):
        # 1. Background
        self.screen.blit(self.bg_surf, (0, 0))

        # 2. Animated Title (Floating effect)
        self.title_float += 0.05
        title_y = 200 + (sin(self.title_float) * 15)
        
        # Draw Title with a "Glow"
        self.draw_text_with_shadow("FARASAT", self.title_font, 'gold', (WIDTH // 2, title_y))
        self.draw_text_with_shadow("AL SAHRAA", self.font, 'white', (WIDTH // 2, title_y + 80))

        # 3. Menu Options
        self.selection_glow += 0.1
        glow_val = abs(sin(self.selection_glow)) * 100 + 155 # Oscillation between 155-255

        for i, option in enumerate(self.menu_options):
            is_selected = i == self.menu_index
            color = (glow_val, glow_val * 0.8, 0) if is_selected else (200, 200, 200)
            
            # Draw Selection Indicators (The "Mirage" brackets)
            if is_selected:
                bracket_offset = 180 + (sin(self.selection_glow * 2) * 5)
                self.draw_text_with_shadow("[", self.font, color, (WIDTH // 2 - bracket_offset, 450 + i * 70))
                self.draw_text_with_shadow("]", self.font, color, (WIDTH // 2 + bracket_offset, 450 + i * 70))

            self.draw_text_with_shadow(option, self.font, color, (WIDTH // 2, 450 + i * 70))

        # 4. Footer
        self.draw_text_with_shadow("A Journey of Insight and Survival", self.subtitle_font, (150, 150, 150), (WIDTH // 2, HEIGTH - 50))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if not self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.menu_index = (self.menu_index - 1) % len(self.menu_options)
                        elif event.key == pygame.K_DOWN:
                            self.menu_index = (self.menu_index + 1) % len(self.menu_options)
                        elif event.key == pygame.K_RETURN:
                            if self.menu_options[self.menu_index] == 'START JOURNEY':
                                self.game_active = True
                            else:
                                pygame.quit()
                                sys.exit()
                else:
                    if event.type == pygame.KEYDOWN:
                        if self.show_tutorial:
                            self.show_tutorial = False
                        else:
                            if event.key == pygame.K_ESCAPE:
                                self.level.toggle_menu()
                            if event.key == pygame.K_b:
                                self.level.toggle_codex()

            if self.game_active:
                self.screen.fill('black')
                self.level.run()
                if self.show_tutorial:
                    self.level.ui.show_tutorial()
            else:
                self.draw_menu()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()