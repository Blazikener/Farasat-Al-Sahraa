import pygame
from support import import_folder
from random import choice
from settings import *

class AnimationPlayer:
	def __init__(self):
		self.frames = {
			# magic
			'flame': import_folder('../graphics/particles/flame/frames'),
			'aura': import_folder('../graphics/particles/aura'),
			'heal': import_folder('../graphics/particles/heal/frames'),
			
			# attacks 
			'claw': import_folder('../graphics/particles/claw'),
			'slash': import_folder('../graphics/particles/slash'),
			'sparkle': import_folder('../graphics/particles/sparkle'),
			'leaf_attack': import_folder('../graphics/particles/leaf_attack'),
			'thunder': import_folder('../graphics/particles/thunder'),

			# monster deaths
			'squid': import_folder('../graphics/particles/smoke_orange'),
			'raccoon': import_folder('../graphics/particles/raccoon'),
			'spirit': import_folder('../graphics/particles/nova'),
			'bamboo': import_folder('../graphics/particles/bamboo'),
			
			# leafs 
			'leaf': (
				import_folder('../graphics/particles/leaf1'),
				import_folder('../graphics/particles/leaf2'),
				import_folder('../graphics/particles/leaf3'),
				import_folder('../graphics/particles/leaf4'),
				import_folder('../graphics/particles/leaf5'),
				import_folder('../graphics/particles/leaf6'),
				self.reflect_images(import_folder('../graphics/particles/leaf1')),
				self.reflect_images(import_folder('../graphics/particles/leaf2')),
				self.reflect_images(import_folder('../graphics/particles/leaf3')),
				self.reflect_images(import_folder('../graphics/particles/leaf4')),
				self.reflect_images(import_folder('../graphics/particles/leaf5')),
				self.reflect_images(import_folder('../graphics/particles/leaf6'))
				)
			}

		# Load only required Tracking Frames for Farasat theme
		self.frames['bamboo_track'] = import_folder('../graphics/particles/tracks/bamboo')
		self.frames['raccoon_track'] = import_folder('../graphics/particles/tracks/raccoon')

	def reflect_images(self,frames):
		new_frames = []
		for frame in frames:
			flipped_surf = pygame.transform.flip(frame,True,False)
			new_frames.append(flipped_surf)
		return new_frames

	def create_grass_particles(self,pos,groups):
		animation_frames = choice(self.frames['leaf'])
		ParticleEffect(pos,animation_frames,groups)

	def create_particles(self,animation_type,pos,groups):
		if animation_type in self.frames and self.frames[animation_type]:
			animation_frames = self.frames[animation_type]
			ParticleEffect(pos,animation_frames,groups,animation_type)

class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,animation_frames,groups,sprite_type = 'magic'):
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.frame_index = 0
		self.animation_speed = 0.15
		self.frames = animation_frames
		
		# Realistic scaling and transparency for tracks
		if 'track' in self.sprite_type:
			self.frames = []
			for frame in animation_frames:
				scaled_frame = pygame.transform.scale(frame, (TILESIZE // 3, TILESIZE // 3))
				scaled_frame.set_alpha(150) # Start semi-transparent
				self.frames.append(scaled_frame)
			self.animation_speed = 0.02 # Make them last longer on screen

		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]
			
			# Perfecting the Fade: Gradually disappear
			if 'track' in self.sprite_type:
				alpha = 150 - (self.frame_index / len(self.frames)) * 150
				self.image.set_alpha(int(alpha))

	def update(self):
		self.animate()