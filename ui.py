import pygame
from settings import *
from math import sin

class UI:
    def __init__(self):
        # General setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(UI_FONT, 36)
        self.insight_font = pygame.font.Font(UI_FONT, 24)

        # Bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Load assets
        self.weapon_graphics = [pygame.image.load(w['graphic']).convert_alpha() for w in weapon_data.values()]
        self.magic_graphics = [pygame.image.load(m['graphic']).convert_alpha() for m in magic_data.values()]

        # Systems
        self.message = ""; self.message_time = 0; self.message_duration = 3000 
        self.transition_alpha = 255 
        
        # Codex Animation
        self.pulse_timer = 0

    def draw_parchment(self, rect):
        """Visual Polish: Draws a textured, ancient-looking paper background."""
        # Main Paper (Parchment color)
        pygame.draw.rect(self.display_surface, '#d4b483', rect)
        # Weathered Edge (Darker tan)
        pygame.draw.rect(self.display_surface, '#a68a56', rect, 8)
        # Gold Border
        pygame.draw.rect(self.display_surface, 'gold', rect.inflate(10, 10), 4)

    def draw_divider(self, x, y, width):
        """Visual Polish: Draws a decorative line with end caps."""
        pygame.draw.line(self.display_surface, '#5c4033', (x, y), (x + width, y), 2)
        pygame.draw.circle(self.display_surface, '#5c4033', (x, y), 4)
        pygame.draw.circle(self.display_surface, '#5c4033', (x + width, y), 4)

    def show_knowledge_book(self, knowledge):
        """An aesthetically beautiful, book-themed Codex."""
        # 1. Darken World Background
        overlay = pygame.Surface((WIDTH, HEIGTH))
        overlay.set_alpha(210)
        overlay.fill('#1a100a')
        self.display_surface.blit(overlay, (0,0))

        # 2. Draw Book Panel
        book_rect = pygame.Rect(WIDTH//4, HEIGTH//10, WIDTH//2, HEIGTH*0.8)
        self.draw_parchment(book_rect)

        # 3. Decorative Title
        title_surf = self.title_font.render("CODEX OF FARASAT", False, '#5c4033')
        self.display_surface.blit(title_surf, title_surf.get_rect(midtop = (WIDTH//2, book_rect.top + 40)))
        self.draw_divider(book_rect.left + 60, book_rect.top + 90, book_rect.width - 120)

        # 4. Categories
        y = book_rect.top + 130
        total_k = 0
        bar_width = book_rect.width - 160
        bar_x = book_rect.left + 80
        
        categories = {
            'terrain': {'icon': 'S', 'color': '#8B4513', 'label': 'TERRAIN INSIGHT'},
            'wildlife': {'icon': 'W', 'color': '#228B22', 'label': 'WILDLIFE INSIGHT'},
            'survival': {'icon': 'E', 'color': '#c2810a', 'label': 'SURVIVAL INSIGHT'}
        }

        for cat_key, info in categories.items():
            value = knowledge[cat_key]
            total_k += value
            
            # Label
            label_surf = self.font.render(f"{info['label']}: {int(value)}%", False, '#5c4033')
            self.display_surface.blit(label_surf, (bar_x, y))
            y += 35
            
            # Progress Bar Background
            bar_bg = pygame.Rect(bar_x, y, bar_width, 22)
            pygame.draw.rect(self.display_surface, '#3d2b1f', bar_bg)
            
            # Progress Bar Fill
            prog_rect = bar_bg.copy()
            prog_rect.width = bar_width * (value / 100)
            pygame.draw.rect(self.display_surface, info['color'], prog_rect)
            
            # Border for Bar
            pygame.draw.rect(self.display_surface, '#5c4033', bar_bg, 2)
            y += 60

        # 5. Total Knowledge (The Pulse of Insight)
        avg_k = total_k / 3
        self.pulse_timer += 0.1
        pulse_val = 150 + (sin(self.pulse_timer) * 50) # Pulses the brightness
        pulse_color = (int(pulse_val), int(pulse_val * 0.8), 0)

        self.draw_divider(book_rect.left + 60, y, book_rect.width - 120)
        y += 40

        total_text = self.font.render(f"TOTAL FARASAT: {int(avg_k)}%", False, '#5c4033')
        self.display_surface.blit(total_text, total_text.get_rect(center = (WIDTH//2, y)))
        
        y += 40
        total_bar = pygame.Rect(bar_x - 20, y, bar_width + 40, 35)
        pygame.draw.rect(self.display_surface, '#222222', total_bar)
        
        prog_total = total_bar.copy()
        prog_total.width = (bar_width + 40) * (avg_k / 100)
        pygame.draw.rect(self.display_surface, pulse_color, prog_total)
        pygame.draw.rect(self.display_surface, 'gold', total_bar, 4)

        # 6. Navigation Hint
        close_surf = self.font.render("Press B to return to the world", False, '#5c4033')
        self.display_surface.blit(close_surf, close_surf.get_rect(center = (WIDTH//2, book_rect.bottom - 40)))

    # --- KEEP OTHER HUD ELEMENTS ---
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

    def show_popup(self, title, lines):
        overlay = pygame.Surface((WIDTH, HEIGTH)); overlay.set_alpha(180); overlay.fill('#000000')
        self.display_surface.blit(overlay, (0,0))
        width, height = 750, 450
        panel_rect = pygame.Rect((WIDTH-width)//2, (HEIGTH-height)//2, width, height)
        self.draw_parchment(panel_rect)
        title_surf = self.title_font.render(title, False, '#5c4033')
        self.display_surface.blit(title_surf, title_surf.get_rect(midtop = (WIDTH//2, panel_rect.top + 30)))
        y = panel_rect.top + 120
        for line in lines:
            line_surf = self.font.render(line, False, '#3d2b1f')
            self.display_surface.blit(line_surf, line_surf.get_rect(center = (WIDTH//2, y))); y += 40
        hint_surf = self.font.render("Press RETURN to continue", False, '#5c4033')
        self.display_surface.blit(hint_surf, hint_surf.get_rect(midbottom = (WIDTH//2, panel_rect.bottom - 30)))

    def draw_transition(self):
        if self.transition_alpha > 0:
            overlay = pygame.Surface((WIDTH, HEIGTH)); overlay.fill('black')
            overlay.set_alpha(self.transition_alpha); self.display_surface.blit(overlay, (0,0))
            self.transition_alpha -= 3

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