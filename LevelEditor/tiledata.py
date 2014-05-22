from pygame import image, color
from pygame.color import *
import pygame, pygame.locals

DEFAULT_TILE_SIZE = 32

#entity keys 
PLAYER_START = "player_start" 

#platforms
PLATFORMS = "platforms"
DEFAULT_PLATFORM = "default_platform"
SLOPING_PLATFORM = "sloping_platform"

#ladders
LADDERS = "ladders"
DEFAULT_LADDER = "default_ladder"

#signs
SIGNS = "signs"
DEFAULT_SIGN = "default_sign"

#lanterns
LANTERNS = "lanterns"
DEFAULT_LANTERN = "default_lantern"

#monsters
MONSTERS = "monsters"
BAT = "bat"
GIANT_FROG = "giant_frog"

#NPCS
NPCS = "NPCs"

#---------TEMPORARY------------------

KENSTAR = "kenstar"

#---------TEMPORARY-------------------

#category map
ENTITY_CATEGORY_MAP = {
	PLAYER_START:None,
	DEFAULT_PLATFORM:PLATFORMS, SLOPING_PLATFORM:PLATFORMS,
	DEFAULT_LADDER:LADDERS,
	DEFAULT_SIGN:DEFAULT_SIGN,
	DEFAULT_LANTERN:LANTERNS, 
	BAT:MONSTERS, GIANT_FROG:MONSTERS,
	#TEMP
	KENSTAR:NPCS
}

#animation key maps

#directions

D_LEFT = "left"
D_RIGHT = "right"
D_DEFAULT = "default"

#animation keys

DEFAULT = "default"
IDLE = "idle"
IDLE_LEFT = "idle_left"
IDLE_RIGHT = "idle_right"

#TODO: as we add more monsters, look for patterns in their animation sets and 
	# generalize these data structures accordingly.

# All animation keys are stored in the form (filename suffix, animation type, direction).
	# example: IDLE_RIGHT, IDLE, D_RIGHT means:
		#1. the filename is [entity name] + IDLE_RIGHT + ".bmp"
		#2. this animation is used when the entity is: 
			# a) idle, and
			# b) when it is facing right.
	# Repetiton is allowed. 
		#for instance, a symmetrical monster may have (IDLE, IDLE, D_LEFT)
			# and also (IDLE, IDLE, D_RIGHT).


DEFAULT_LANTERN_ANIMATION_KEYS = [
	(DEFAULT, DEFAULT, D_DEFAULT),
]

DEFAULT_MONSTER_ANIMATION_KEYS = [
	(IDLE_LEFT, IDLE, D_DEFAULT),
	(IDLE_LEFT,  IDLE, D_LEFT), 
	(IDLE_RIGHT, IDLE, D_RIGHT)
]

DEFAULT_NPC_ANIMATION_KEYS = [
	(IDLE_LEFT, IDLE, D_DEFAULT),
	(IDLE_LEFT,  IDLE, D_LEFT), 
	(IDLE_RIGHT, IDLE, D_RIGHT)
]

# Note that not every monster needs an animation key set.
	# We can use default(s) for monsters whose animation key sets
	# are not shown here, based on their type if necessary.

BAT_ANIMATION_KEYS = [
	(IDLE, IDLE, D_DEFAULT),
	(IDLE, IDLE, D_LEFT),
	(IDLE, IDLE, D_RIGHT) 
	]

ANIMATION_KEY_MAP = {
	DEFAULT_LANTERN:DEFAULT_LANTERN_ANIMATION_KEYS,
	BAT:BAT_ANIMATION_KEYS
}

CATEGORY_ANIMATION_KEY_MAP = {
	MONSTERS:DEFAULT_MONSTER_ANIMATION_KEYS, 
	NPCS:DEFAULT_NPC_ANIMATION_KEYS
}

class TileData(object):

	"""docstring for TileData"""
	def __init__(self, key, filepath, filepath_start = "./"):
		self.entity_key = key #could also set some values using this
		self.image_filepath = filepath
		self.width, self.height = 1, 1
		self.setDimensions(filepath_start)

	def create_copy(self):
		return TileData(self.entity_key, self.image_filepath)

	def setDimensions(self, filepath_start):
		image = self.get_image(filepath_start)
		self.width = image.get_width()/DEFAULT_TILE_SIZE
		self.height = image.get_height()/DEFAULT_TILE_SIZE

	def get_image(self, filepath_start = "./"):	#TODO: consider allowing filepath beginning here.
		filepath = filepath_start + self.image_filepath
		return TileData.load_image (filepath)

	@staticmethod
	def load_image (filename, alpha = False, colorkey = None):
		"""
		NOTE: copied from ocempgui.
		"""
		surface = image.load(filename)
		if colorkey:
			surface.set_colorkey (colorkey)
		if alpha or surface.get_alpha ():
			return surface.convert_alpha ()
		return surface.convert ()

	def category(self):
		return ENTITY_CATEGORY_MAP[self.entity_key]

	def is_animated(self):
		return (self.entity_key in ANIMATION_KEY_MAP or 
				self.category() in CATEGORY_ANIMATION_KEY_MAP)

	def animation_filepath(self, filepath_start = "./"): #TODO
		filepath = filepath_start + "animations"
		key = self.entity_key
		if key not in ENTITY_CATEGORY_MAP or key == None: 
			return None
		filepath += "/" + self.category() + "/" + key + "/"
		return filepath

	def animation_keys(self):
		key = self.entity_key
		if key in ANIMATION_KEY_MAP:
			return ANIMATION_KEY_MAP[key]
		if self.category() in CATEGORY_ANIMATION_KEY_MAP:
			return CATEGORY_ANIMATION_KEY_MAP[self.category()]
		return None

	# TODO: make sure SignData can be formatted and deformatted properly.

	def formatted_data(self):
		return (self.entity_key, self.image_filepath, self.width, self.height) 

	@staticmethod
	def deformatted_tile_set(formatted_data, filepath = "./"):
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
					TileData.addTiles(tiles, next_tile, x, y, filepath)
		return tiles

	@staticmethod
	def addTiles(tiles, formatted_data, x_pos, y_pos, filepath = "./"):
		width = formatted_data[2]
		height = formatted_data[3]
		origin_tile = TileData.deformatted_tile(formatted_data, filepath)
		tiles[y_pos][x_pos] = origin_tile
		for x in range(x_pos + 1, x_pos + width):
			tiles[y_pos][x] = BlockedTileData(origin_tile, x_pos, y_pos)
		for y in range(y_pos + 1, y_pos + height):
			for x in range(x_pos, x_pos + width):
				tiles[y][x] = BlockedTileData(origin_tile, x_pos, y_pos)

	@staticmethod
	def deformatted_tile(formatted_data, filepath = "./"):	#this will need to change as this class's constructor does.
		entity_key = formatted_data[0]
		tile_data = TileData(formatted_data[0], formatted_data[1], filepath)
		if entity_key in TILE_INIT_MAP:
			init_function = TILE_INIT_MAP[entity_key] #TODO: get a constructor from a map
			init_function(tile_data, formatted_data)
		return tile_data
		#return TileData(formatted_data[0], formatted_data[1], filepath)

	@staticmethod
	def deformatted_sign(sign_data, formatted_data):	#this will need to change as this class's constructor does.
		sign_data.text_panes = formatted_data[4]

class BlockedTileData(TileData): #this is a space in a room's tiles blocked out by some object that takes up more than one tile.
	def __init__(self, origin_tile, x, y):
		self.origin_tile = origin_tile
		self.origin_x, self.origin_y = x, y

	def formatted_data(self):
		return None

TILE_INIT_MAP = {
	DEFAULT_SIGN:TileData.deformatted_sign
}