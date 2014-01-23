from pygame import *
import pygame, pygame.locals
from ocempgui.draw import Image

DEFAULT_TILE_SIZE = 32

#TODO: use these for mapping entity keys to the data used to build entities
PLAYER_START = "player_start" 

DEFAULT_PLATFORM = "default_platform"

BAT = "bat"
GIANT_FROG = "giant_frog"

class TileData(object):

	"""docstring for TileData"""
	def __init__(self, key, filepath,filepath_start = "./"):
		self.entity_key = key #could also set some values using this
		self.image_filepath = filepath
		self.width, self.height = 1,1
		self.setDimensions(filepath_start)

	def setDimensions(self,filepath_start):
		image = self.get_image(filepath_start)
		self.width = image.get_width()/DEFAULT_TILE_SIZE
		self.height = image.get_height()/DEFAULT_TILE_SIZE

	def get_image(self,filepath_start = "./"):	#TODO: consider allowing filepath beginning here.
		filepath = filepath_start+self.image_filepath
		return Image.load_image (filepath)

	#def get_animation_set(self,filepath_start = "./"): #TODO
	#	key = self.entity_key
	#	if key not in ANIMATION_MAP: return None
	#	return ANIMATION_MAP[key]

	def formatted_data(self):
		return (self.entity_key,self.image_filepath, self.width, self.height) 

	@staticmethod
	def deformatted_tile_set(formatted_data,filepath = "./"):
		tiles = []
		for y in xrange (len(formatted_data)):
			tiles.append([])
			for x in xrange(len(formatted_data[y])):
				tiles[y].append(None)
		for y in xrange(len(formatted_data)):
			for x in xrange(len(formatted_data[y])):
				next_data = None
				next_tile = formatted_data[y][x]
				if next_tile != None:
					TileData.addTiles(tiles,next_tile,x,y,filepath)
		return tiles

	@staticmethod
	def addTiles(tiles,formatted_data,x_pos,y_pos,filepath = "./"):
		width = formatted_data[2]
		height = formatted_data[3]
		origin_tile = TileData.deformatted_tile(formatted_data,filepath)
		tiles[y_pos][x_pos] = origin_tile
		for x in range(x_pos + 1, x_pos + width):
			tiles[y_pos][x] = BlockedTileData(origin_tile,x_pos,y_pos)
		for y in range(y_pos + 1,y_pos + height):
			for x in range(x_pos, x_pos + width):
				tiles[y][x] = BlockedTileData(origin_tile,x_pos,y_pos)

	@staticmethod
	def deformatted_tile(formatted_data,filepath = "./"):	#this will need to change as this class's constructor does.
		return TileData(formatted_data[0],formatted_data[1],filepath)


class BlockedTileData(TileData): #this is a space in a room's tiles blocked out by some object that takes up more than one tile.
	def __init__(self,origin_tile,x,y):
		self.origin_tile = origin_tile
		self.origin_x, self.origin_y = x,y

	def formatted_data(self):
		return None

