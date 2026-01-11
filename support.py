from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []
	valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')

	for _,__,img_files in walk(path):
		# Sort files to ensure they load in the correct order (important for animations)
		img_files.sort() 
		for image in img_files:
			if image.lower().endswith(valid_extensions):
				full_path = path + '/' + image
				try:
					image_surf = pygame.image.load(full_path).convert_alpha()
					surface_list.append(image_surf)
				except pygame.error as e:
					print(f"Failed to load image at {full_path}: {e}")
			else:
				# Skips non-image files like Thumbs.db or .txt files
				continue

	return surface_list