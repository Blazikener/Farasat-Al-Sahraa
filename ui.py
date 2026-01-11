import pygame
from settings import *
from math import sin

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(UI_FONT, 36)
        self.insight_font = pygame.font.Font(UI_FONT, 24)
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        self.weapon_graphics = [pygame.image.load(w['graphic']).convert_alpha() for w in weapon_data.values()]
        self.weapon_names = list(weapon_data.keys())
        self.magic_graphics = [pygame.image.load(m['graphic']).convert_alpha() for m in magic_data.values()]
        
        try:
            self.shop_icon_surf = pygame.image.load('../graphics/ui/shop_icon.png').convert_alpha()
            self.shop_icon_surf = pygame.transform.scale(self.shop_icon_surf, (40, 40))
        except:
            self.shop_icon_surf = pygame.Surface((40, 40)); self.shop_icon_surf.fill('gold')

        self.message = ""; self.message_time = 0; self.message_duration = 3000 
        self.transition_alpha = 255; self.pulse_timer = 0

    def draw_parchment(self, rect):
        pygame.draw.rect(self.display_surface, '#d4b483', rect)
        pygame.draw.rect(self.display_surface, '#a68a56', rect, 8)
        pygame.draw.rect(self.display_surface, 'gold', rect.inflate(10, 10), 4)

    def trigger_insight(self, text):
        self.message = text; self.message_time = pygame.time.get_ticks()

    def draw_insight_message(self):
        current_time = pygame.time.get_ticks()
        if self.message and current_time - self.message_time < self.message_duration:
            elapsed = current_time - self.message_time; alpha = 255
            if elapsed > 2000: alpha = 255 - int(((elapsed - 2000) / 1000) * 255)
            text_surf = self.insight_font.render(f"INSIGHT: {self.message}", False, 'gold')
            text_surf.set_alpha(alpha); text_rect = text_surf.get_rect(center = (WIDTH // 2, HEIGTH - 100))
            bg_surf = pygame.Surface((text_rect.width + 30, text_rect.height + 20), pygame.SRCALPHA)
            bg_surf.fill((0, 0, 0, int(alpha * 0.6)))
            self.display_surface.blit(bg_surf, text_rect.inflate(30, 20)); self.display_surface.blit(text_surf, text_rect)

    def show_tutorial(self):
        """The Restored Introduction Overlay."""
        overlay = pygame.Surface((WIDTH, HEIGTH)); overlay.set_alpha(230); overlay.fill('#0a0a0a')
        self.display_surface.blit(overlay, (0,0))
        self.display_surface.blit(self.title_font.render("JOURNEY OF INSIGHT", False, 'gold'), (WIDTH//2 - 190, 100))
        
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
            self.display_surface.blit(surf, surf.get_rect(center = (WIDTH//2, y))); y += 40

    def show_shop(self, player, current_index):
        overlay = pygame.Surface((WIDTH, HEIGTH)); overlay.set_alpha(210); overlay.fill('#1a100a'); self.display_surface.blit(overlay, (0,0))
        shop_rect = pygame.Rect(WIDTH//4, HEIGTH//10, WIDTH//2, HEIGTH*0.8); self.draw_parchment(shop_rect)
        self.display_surface.blit(self.title_font.render("THE DESERT TRADER", False, '#5c4033'), (WIDTH//2 - 180, shop_rect.top + 40))
        self.display_surface.blit(self.font.render(f"AVAILABLE SCRAPS: {int(player.exp)}", False, '#8B4513'), (WIDTH//2 - 140, shop_rect.top + 90))
        for i, name in enumerate(self.weapon_names):
            if name == 'sword': continue
            y_pos = shop_rect.top + 160 + (i-1) * 100
            item_rect = pygame.Rect(shop_rect.left + 50, y_pos, shop_rect.width - 100, 80)
            is_sel = i == current_index
            pygame.draw.rect(self.display_surface, '#c2a373' if is_sel else '#d4b483', item_rect)
            pygame.draw.rect(self.display_surface, 'gold' if is_sel else '#5c4033', item_rect, 3)
            icon = self.weapon_graphics[i]; self.display_surface.blit(icon, icon.get_rect(midleft = (item_rect.left + 20, item_rect.centery)))
            status = "OWNED" if name in player.unlocked_weapons else f"COST: {weapon_data[name].get('cost', 150)}"
            self.display_surface.blit(self.font.render(name.upper(), False, '#3d2b1f'), (item_rect.left + 100, item_rect.top + 15))
            self.display_surface.blit(self.font.render(status, False, '#5c4033'), (item_rect.left + 100, item_rect.top + 45))
        self.display_surface.blit(self.font.render("ARROWS: Navigate | SPACE: Buy | V: Close", False, '#5c4033'), (WIDTH//2 - 200, shop_rect.bottom - 40))

    def show_knowledge_book(self, knowledge):
        overlay = pygame.Surface((WIDTH, HEIGTH)); overlay.set_alpha(210); overlay.fill('#1a100a'); self.display_surface.blit(overlay, (0,0))
        book_rect = pygame.Rect(WIDTH//4, HEIGTH//10, WIDTH//2, HEIGTH*0.8); self.draw_parchment(book_rect)
        self.display_surface.blit(self.title_font.render("CODEX OF FARASAT", False, '#5c4033'), (WIDTH//2 - 160, book_rect.top + 40))
        y = book_rect.top + 130; total_k = 0; bar_width = book_rect.width - 160; bar_x = book_rect.left + 80
        cats = {'terrain': '#8B4513', 'wildlife': '#228B22', 'survival': '#c2810a'}
        for key, color in cats.items():
            val = knowledge[key]; total_k += val
            self.display_surface.blit(self.font.render(f"{key.upper()} INSIGHT: {int(val)}%", False, '#5c4033'), (bar_x, y)); y += 35
            pygame.draw.rect(self.display_surface, '#3d2b1f', (bar_x, y, bar_width, 22))
            pygame.draw.rect(self.display_surface, color, (bar_x, y, bar_width * (val/100), 22))
            pygame.draw.rect(self.display_surface, '#5c4033', (bar_x, y, bar_width, 22), 2); y += 60
        avg_k = total_k / 3; self.pulse_timer += 0.08; pulse = 160 + (sin(self.pulse_timer) * 60)
        total_bar = pygame.Rect(bar_x - 20, y + 40, bar_width + 40, 35); pygame.draw.rect(self.display_surface, '#222222', total_bar)
        pygame.draw.rect(self.display_surface, (int(pulse), int(pulse*0.8), 0), (bar_x - 20, y + 40, (bar_width + 40) * (avg_k/100), 35))
        pygame.draw.rect(self.display_surface, 'gold', total_bar, 4)
        self.display_surface.blit(self.font.render("Press B to return", False, '#5c4033'), (WIDTH//2 - 80, book_rect.bottom - 40))

    def show_popup(self, title, lines):
        overlay = pygame.Surface((WIDTH, HEIGTH)); overlay.set_alpha(180); overlay.fill('#000000'); self.display_surface.blit(overlay, (0,0))
        rect = pygame.Rect((WIDTH-750)//2, (HEIGTH-450)//2, 750, 450); self.draw_parchment(rect)
        self.display_surface.blit(self.title_font.render(title, False, '#5c4033'), (WIDTH//2 - 120, rect.top + 30))
        y = rect.top + 120
        for line in lines:
            surf = self.font.render(line, False, '#3d2b1f'); self.display_surface.blit(surf, surf.get_rect(center = (WIDTH//2, y))); y += 45
        self.display_surface.blit(self.font.render("Press RETURN to continue", False, '#5c4033'), (WIDTH//2 - 120, rect.bottom - 40))

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        ratio = current / max_amount
        cur_rect = bg_rect.copy(); cur_rect.width = bg_rect.width * ratio
        pygame.draw.rect(self.display_surface, color, cur_rect); pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def draw_transition(self):
        if self.transition_alpha > 0:
            overlay = pygame.Surface((WIDTH, HEIGTH)); overlay.fill('black'); overlay.set_alpha(self.transition_alpha)
            self.display_surface.blit(overlay, (0,0)); self.transition_alpha -= 4

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        slots = [(10, 'Q', player.weapon_index), (100, 'E', player.magic_index)]
        for x, key, idx in slots:
            rect = pygame.Rect(x, 630, ITEM_BOX_SIZE, ITEM_BOX_SIZE); pygame.draw.rect(self.display_surface, UI_BG_COLOR, rect)
            surf = self.weapon_graphics[idx] if key == 'Q' else self.magic_graphics[idx]
            self.display_surface.blit(surf, surf.get_rect(center = rect.center)); pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, rect, 3)
            self.display_surface.blit(self.font.render(key, False, 'gold'), (rect.right - 22, rect.bottom - 22))
        
        # Currency/Shop Indicator
        icon_rect = pygame.Rect(WIDTH - 220, 10, 200, 50); pygame.draw.rect(self.display_surface, UI_BG_COLOR, icon_rect)
        pygame.draw.rect(self.display_surface, 'gold', icon_rect, 2); self.display_surface.blit(self.shop_icon_surf, (icon_rect.left + 5, icon_rect.top + 5))
        self.display_surface.blit(self.font.render(f"SCRAPS: {int(player.exp)}", False, 'white'), (icon_rect.left + 50, icon_rect.top + 15))
        
        self.draw_insight_message(); self.draw_transition()