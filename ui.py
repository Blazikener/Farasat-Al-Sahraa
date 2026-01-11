import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(UI_FONT, 32)
        self.insight_font = pygame.font.Font(UI_FONT, 24)

        # Bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Assets
        self.weapon_graphics = [pygame.image.load(w['graphic']).convert_alpha() for w in weapon_data.values()]
        self.magic_graphics = [pygame.image.load(m['graphic']).convert_alpha() for m in magic_data.values()]

        # Systems
        self.message = ""; self.message_time = 0; self.message_duration = 3000 
        self.transition_alpha = 255 

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        ratio = current / max_amount
        current_rect = bg_rect.copy()
        current_rect.width = bg_rect.width * ratio
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def trigger_insight(self, text):
        self.message = text
        self.message_time = pygame.time.get_ticks()

    def draw_insight_message(self):
        current_time = pygame.time.get_ticks()
        if self.message and current_time - self.message_time < self.message_duration:
            elapsed = current_time - self.message_time
            alpha = 255
            if elapsed > 2000: alpha = 255 - int(((elapsed - 2000) / 1000) * 255)
            text_surf = self.insight_font.render(f"INSIGHT: {self.message}", False, 'gold')
            text_surf.set_alpha(alpha)
            text_rect = text_surf.get_rect(center = (WIDTH // 2, HEIGTH - 100))
            bg_rect = text_rect.inflate(30, 20)
            bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surf.fill((0, 0, 0, int(alpha * 0.6)))
            self.display_surface.blit(bg_surf, bg_rect)
            self.display_surface.blit(text_surf, text_rect)

    def draw_transition(self):
        if self.transition_alpha > 0:
            overlay = pygame.Surface((WIDTH, HEIGTH)); overlay.fill('black')
            overlay.set_alpha(self.transition_alpha); self.display_surface.blit(overlay, (0,0))
            self.transition_alpha -= 3

    def show_tutorial(self):
        overlay = pygame.Surface((WIDTH, HEIGTH)); overlay.set_alpha(220); overlay.fill('#0a0a0a')
        self.display_surface.blit(overlay, (0,0))
        title_surf = self.title_font.render("JOURNEY OF INSIGHT", False, 'gold')
        self.display_surface.blit(title_surf, title_surf.get_rect(center = (WIDTH//2, 100)))
        instructions = ["ARROWS: Move", "SPACE: Attack/Interact", "L-CTRL: Magic", "Q: Switch Weapon", "E: Switch Ability", "B: Codex", "-----------------", "Insight is Knowledge.", "Unlock zones by observing the world.", "-----------------", "PRESS ANY KEY TO START"]
        y = 180
        for line in instructions:
            text = self.font.render(line, False, 'white')
            self.display_surface.blit(text, text.get_rect(center = (WIDTH//2, y))); y += 35

    def show_knowledge_book(self, knowledge):
        overlay = pygame.Surface((WIDTH, HEIGTH)); overlay.set_alpha(200); overlay.fill('#1a100a'); self.display_surface.blit(overlay, (0,0))
        book_rect = pygame.Rect(WIDTH//4, HEIGTH//8, WIDTH//2, HEIGTH*0.75)
        pygame.draw.rect(self.display_surface, '#3d2b1f', book_rect); pygame.draw.rect(self.display_surface, 'gold', book_rect, 5)
        title_surf = self.title_font.render("CODEX OF FARASAT", False, 'gold')
        self.display_surface.blit(title_surf, title_surf.get_rect(midtop = (WIDTH//2, book_rect.top + 30)))
        y = book_rect.top + 100; total_k = 0; bar_width = book_rect.width - 100; bar_x = book_rect.left + 50
        for category, value in knowledge.items():
            total_k += value
            self.display_surface.blit(self.font.render(f"{category.upper()}: {int(value)}%", False, 'white'), (bar_x, y)); y += 30
            bar_rect = pygame.Rect(bar_x, y, bar_width, 25); pygame.draw.rect(self.display_surface, UI_BG_COLOR, bar_rect)
            progress_rect = bar_rect.copy(); progress_rect.width = bar_width * (value / 100)
            color = '#8B4513' if category == 'terrain' else '#228B22' if category == 'wildlife' else '#FFD700'
            pygame.draw.rect(self.display_surface, color, progress_rect); pygame.draw.rect(self.display_surface, 'white', bar_rect, 2); y += 50
        avg_k = total_k / 3
        total_bar = pygame.Rect(bar_x, y + 20, bar_width, 30); pygame.draw.rect(self.display_surface, UI_BG_COLOR, total_bar)
        prog_rect = total_bar.copy(); prog_rect.width = bar_width * (avg_k / 100); pygame.draw.rect(self.display_surface, 'gold', prog_rect)
        pygame.draw.rect(self.display_surface, 'gold', total_bar, 3)

    def weapon_overlay(self, weapon_index):
        bg_rect = pygame.Rect(10, 630, ITEM_BOX_SIZE, ITEM_BOX_SIZE); pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        weapon_surf = self.weapon_graphics[weapon_index]; self.display_surface.blit(weapon_surf, weapon_surf.get_rect(center = bg_rect.center))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        self.display_surface.blit(self.font.render("Q", False, 'gold'), (bg_rect.right - 20, bg_rect.bottom - 20))

    def magic_overlay(self, magic_index):
        bg_rect = pygame.Rect(100, 630, ITEM_BOX_SIZE, ITEM_BOX_SIZE); pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        magic_surf = self.magic_graphics[magic_index]; self.display_surface.blit(magic_surf, magic_surf.get_rect(center = bg_rect.center))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        self.display_surface.blit(self.font.render("E", False, 'gold'), (bg_rect.right - 20, bg_rect.bottom - 20))

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.weapon_overlay(player.weapon_index); self.magic_overlay(player.magic_index)
        self.draw_insight_message(); self.draw_transition()