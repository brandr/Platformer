from pygame import *
import pygame, pygame.locals
from ocempgui.draw import Image

#TODO: use these for mapping entity keys to the data used to build entities
PLAYER_START = "player_start" 

DEFAULT_PLATFORM = "default_platform"

BAT = "bat"
GIANT_FROG = "giant_frog"

class TileData(object):
	"""docstring for TileData"""
	def __init__(self, key, filepath):
		self.entity_key = key #could also set some values using this
		self.image_filepath = filepath

	def get_image(self,filepath_start = "./"):	#TODO: consider allowing filepath beginning here.
		filepath = filepath_start+self.image_filepath
		return Image.load_image (filepath)

	def formatted_data(self):
		return (self.entity_key,self.image_filepath) #currently, will have to recreate tiledata using just this key. may need more later.

	@staticmethod
	def deformatted_tile_set(formatted_data):
		tiles = []
		for y in xrange (len(formatted_data)):
			tiles.append([])
			for x in xrange(len(formatted_data[y])):
				next_data = None
				next_tile = formatted_data[y][x]
				if next_tile != None:
					next_data = TileData.deformatted_tile(next_tile)
				tiles[y].append(next_data)
		return tiles

	@staticmethod
	def deformatted_tile(formatted_data):	#this will need to change as this class's constructor does.
		return TileData(formatted_data[0],formatted_data[1])