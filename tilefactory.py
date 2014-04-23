import pygame
from pygame import *
import gameimage
from gameimage import *

class TileFactory(object):

	#this setup might be useful for reading in an entire level of tiles, which in turn is read in from an image.
	def __init__(self, tile_sheet_image, dimensions):
		self.tile_images = []
		default_rect = Rect(0, 0, 32, 32)
		tile_sheet = SpriteSheet(tile_sheet_image, default_rect)
		current_rect = default_rect
		for y in range(0, dimensions[1]): #TODO: make it possible to move rect down for y > 1
			current_rect = Rect(0, y*32, 32, 32)
			self.tile_images.append([])
			next_row = tile_sheet.load_strip(default_rect, dimensions[0])
			for image in next_row:
				self.tile_images[y].append(image)

	def image_at(self, coords):
		return self.tile_images[coords[1]][coords[0]]
	
	def tile_at(self, coords):
		tile_image = self.image_at(coords)
		return GameImage.still_animation_set(tile_image)