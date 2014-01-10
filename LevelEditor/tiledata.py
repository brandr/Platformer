from pygame import *
import pygame, pygame.locals
from ocempgui.draw import Image

PLATFORMS = "platforms"
MONSTERS = "monsters"
PLAYER_START = "player_start"
PRIMARY_ENTITY_NAMES = (PLATFORMS,MONSTERS,PLAYER_START)

DEFAULT_PLATFORM,FIRE_PLATFORM = "default_platform","fire_platform"
PLATFORM_NAMES = (DEFAULT_PLATFORM,FIRE_PLATFORM)

BAT,GIANT_FROG = "bat","giant_frog"
MONSTER_NAMES = (BAT,GIANT_FROG)
#MONSTERS = (BAT,GIANT FROG) #could potentially do something like this
PRIMARY_ENTITY_MAP = {PLATFORMS:PLATFORM_NAMES, MONSTERS:MONSTER_NAMES} #could potentially map category names to more maps, rather than name lists.

SELECTABLE_ENTITY_MAP = {DEFAULT_PLATFORM:"default_platform.bmp",FIRE_PLATFORM:"fire_platform.bmp",
						BAT:"bat.bmp", GIANT_FROG:"giant_frog.bmp",PLAYER_START:"player_start.bmp"}	#TODO: find a good way to organize more data than this, since we want to map to actual objects, not just image filenames.

class TileData(object):
	"""docstring for TileData"""
	def __init__(self, key):
		self.entity_key = key #could also set some values using this
		self.tile_image = Surface((32,32)) #could  make a static blank tile arg
		self.tile_image.fill(Color("#FFFFFF"))
		self.setImage(key)

	def setImage(self,key):
		filename = SELECTABLE_ENTITY_MAP[key]
		entity_image = Image.load_image ("./LevelEditor/images/"+filename) #this directory might not always work
		self.tile_image.blit(entity_image,(0,0))

	def get_image(self):
		return self.tile_image

	def formatted_data(self):
		return self.entity_key #currently, will have to recreate tiledata using just this key. may need more later.

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
		return TileData(formatted_data)