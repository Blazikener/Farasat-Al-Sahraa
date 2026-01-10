import pygame
from settings import *

class UI:
	def __init__(self):
		
		# general 
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

		# bar setup 
		self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

		# load assets
		self.weapon_graphics = [pygame.image.load(w['graphic']).convert_alpha() for w in weapon_data.values()]
		self.magic_graphics = [pygame.image.load(m['graphic']).convert_alpha() for m in magic_data.values()]
		self.insight_icon = pygame.image.load('../graphics/ui/insight_icon.png').convert_alpha()


	def show_bar(self,current,max_amount,bg_rect,color):
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
		ratio = current / max_amount
		current_rect = bg_rect.copy()
		current_rect.width = bg_rect.width * ratio
		pygame.draw.rect(self.display_surface,color,current_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

	def show_study_bar(self, progress, target):
		if 0 < progress < target:
			width, height = 400, 15
			x = (self.display_surface.get_size()[0] // 2) - (width // 2)
			y = self.display_surface.get_size()[1] - 120
			bg_rect = pygame.Rect(x,y,width,height)
			pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
			current_rect = pygame.Rect(x,y,width * (progress/target),height)
			pygame.draw.rect(self.display_surface, 'gold', current_rect)
			pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
			text_surf = self.font.render("Interpreting Environment...", False, TEXT_COLOR)
			text_rect = text_surf.get_rect(midbottom = (x + width//2, y - 10))
			self.display_surface.blit(text_surf, text_rect)

	def show_insight_indicator(self, player):
		"""Visual cue for Ethical Study mechanic."""
		icon_rect = self.insight_icon.get_rect(midbottom = player.rect.midtop - pygame.math.Vector2(0, 10))
		self.display_surface.blit(self.insight_icon, icon_rect)

	def show_exp(self,exp):
		text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
		x, y = self.display_surface.get_size()[0] - 20, self.display_surface.get_size()[1] - 20
		text_rect = text_surf.get_rect(bottomright = (x,y))
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
		self.display_surface.blit(text_surf,text_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

	def selection_box(self,left,top, has_switched):
		bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
		color = UI_BORDER_COLOR_ACTIVE if has_switched else UI_BORDER_COLOR
		pygame.draw.rect(self.display_surface,color,bg_rect,3)
		return bg_rect

	def display(self,player):
		self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
		self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)
		self.show_exp(player.exp)
		self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
		self.magic_overlay(player.magic_index,not player.can_switch_magic)

	def weapon_overlay(self,weapon_index,has_switched):
		bg_rect = self.selection_box(10,630,has_switched)
		self.display_surface.blit(self.weapon_graphics[weapon_index], self.weapon_graphics[weapon_index].get_rect(center = bg_rect.center))

	def magic_overlay(self,magic_index,has_switched):
		bg_rect = self.selection_box(80,635,has_switched)
		self.display_surface.blit(self.magic_graphics[magic_index], self.magic_graphics[magic_index].get_rect(center = bg_rect.center))