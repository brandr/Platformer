from pygame import *
import pygame, pygame.locals
from ocempgui.draw import Image

PLATFORMS = "platforms"
MONSTERS = "monsters"
PRIMARY_ENTITY_NAMES = (PLATFORMS,MONSTERS)

DEFAULT_PLATFORM,FIRE_PLATFORM = "default_platform","fire_platform"
PLATFORM_NAMES = (DEFAULT_PLATFORM,FIRE_PLATFORM)

BAT,GIANT_FROG = "bat","giant_frog"
MONSTER_NAMES = (BAT,GIANT_FROG)
#MONSTERS = (BAT,GIANT FROG) #could potentially do something like this
PRIMARY_ENTITY_MAP = {PLATFORMS:PLATFORM_NAMES, MONSTERS:MONSTER_NAMES} #could potentially map category names to more maps, rather than name lists.

SELECTABLE_ENTITY_MAP = {DEFAULT_PLATFORM:"default_platform.bmp",FIRE_PLATFORM:"fire_platform.bmp",
						BAT:"bat.bmp", GIANT_FROG:"giant_frog.bmp"}	#TODO: find a good way to organize more data than this, since we want to map to actual objects, not just image filenames.

class TileData(object):
	"""docstring for TileData"""
	def __init__(self, key):
		self.tile_image = Surface((32,32)) #could  make a static blank tile arg
		self.tile_image.fill(Color("#FFFFFF"))
		self.setImage(key)

	def setImage(self,key):
		filename = SELECTABLE_ENTITY_MAP[key]
		entity_image = Image.load_image ("./images/"+filename)
		self.tile_image.blit(entity_image,(0,0))

	def get_image(self):
		return self.tile_image