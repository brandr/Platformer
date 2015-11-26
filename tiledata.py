""" A data object used to build a tile (and the entity in it, if there is one).
"""

from pygame import image, Rect
import pygame, pygame.locals
from gameimage import GameImage, DEFAULT_COLORKEY
from animationset import AnimationSet

DEFAULT_TILE_SIZE = 32

#entity keys 
PLAYER_START = "player_start" 

#platforms
PLATFORMS = "platforms"
DEFAULT_PLATFORM = "default_platform"
SLOPING_PLATFORM = "sloping_platform"
DESTRUCTIBLE_PLATFORM = "destructible_platform"
PASSABLE_PLATFORM = "passable_platform"

#ladders
LADDERS = "ladders"
DEFAULT_LADDER = "default_ladder"

#signs
SIGNS = "signs"
DEFAULT_SIGN = "default_sign"

#doors
DOORS = "doors"
DEFAULT_DOOR = "default_door"

#lanterns
LANTERNS = "lanterns"
DEFAULT_LANTERN = "default_lantern"

#chests
CHESTS = "chests"
DEFAULT_CHEST = "default_chest"

#pickups
PICKUPS = "pickups"
OIL_PICKUP = "oil_pickup"

#monsters
MONSTERS = "monsters"
BAT = "bat"
GIANT_FROG = "giant_frog"
ARMORED_FROG = "armored_frog"

#NPCS
NPCS = "NPCs"
DEFAULT_NPC = "default_npc"
MINER = "miner"

#save points
SAVE_POINTS = "save_points"
DEFAULT_SAVE_POINT = "save_point"

#triggers
TRIGGERS = "triggers"
DEFAULT_CUTSCENE_TRIGGER = "default_cutscene_trigger"

#Level effects
LEVEL_EFFECTS = "level_effects"
DEFAULT_LEVEL_EFFECT = "default_level_effect"

#---------TEMPORARY------------------

KENSTAR = "kenstar"

#---------TEMPORARY-------------------

#category map
ENTITY_CATEGORY_MAP = {
	PLAYER_START:None,
	DEFAULT_PLATFORM:PLATFORMS, SLOPING_PLATFORM:PLATFORMS, DESTRUCTIBLE_PLATFORM:PLATFORMS, PASSABLE_PLATFORM:PLATFORMS,
	DEFAULT_LADDER:LADDERS,
	DEFAULT_SIGN:SIGNS,
	DEFAULT_DOOR:DOORS,
	DEFAULT_LANTERN:LANTERNS, 
	DEFAULT_CHEST:CHESTS,
	OIL_PICKUP:PICKUPS,
	BAT:MONSTERS, GIANT_FROG:MONSTERS, ARMORED_FROG:MONSTERS,
	DEFAULT_NPC:NPCS, MINER:NPCS,
	DEFAULT_SAVE_POINT:SAVE_POINTS,
	DEFAULT_CUTSCENE_TRIGGER:TRIGGERS,
	DEFAULT_LEVEL_EFFECT:LEVEL_EFFECTS,
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

SWINGING = "swinging"
SWINGING_LEFT = "swinging_left"
SWINGING_RIGHT = "swinging_right"

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

MINER_ANIMATION_KEYS = [
	(IDLE_LEFT, IDLE, D_DEFAULT, 20),
	(IDLE_LEFT,  IDLE, D_LEFT, 20), 
	(IDLE_RIGHT, IDLE, D_RIGHT, 20),
	(SWINGING_LEFT, SWINGING, D_LEFT),
	(SWINGING_RIGHT, SWINGING, D_RIGHT)
]

# DEFAULTS

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

DEFAULT_EFFECT_ANIMATION_KEYS = [
	(DEFAULT, DEFAULT, D_DEFAULT)
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
	BAT:BAT_ANIMATION_KEYS,
	MINER:MINER_ANIMATION_KEYS
	#DEFAULT_LEVEL_EFFECT:DEFAULT_EFFECT_ANIMATION_KEY
}

CATEGORY_ANIMATION_KEY_MAP = {
	MONSTERS:DEFAULT_MONSTER_ANIMATION_KEYS, 
	NPCS:DEFAULT_NPC_ANIMATION_KEYS,
	LEVEL_EFFECTS:DEFAULT_EFFECT_ANIMATION_KEYS
}

class TileData(object):
	""" TileData( str, str, str ) -> TileData

	TileDatas operate based on string keys that are used to access the proper animations/data
	from various dicts.

	Attributes:

	entity_key: A string key used to build the Tile.

	image_filepath: The filepath that the tile's image is loaded from.

	width, height: The dimensions of the entity in the tile (if there is one). Note that these dimensions are not for the tile itself,
	since all tiles are the same width and heigh.
	"""
	def __init__(self, key, filepath, filepath_start = "./"):
		self.entity_key = key 				# could also set more values using this key if necessary
		self.image_filepath = filepath
		self.width, self.height = 1, 1
		self.setDimensions(filepath_start)

	def setDimensions(self, filepath_start):
		""" td.setDimensions( str ) -> None

		Take the image associated with this tiledata and figure out the associated entity's dimensions based on the image's dimensions.
		"""
		image = self.get_image(filepath_start)
		self.width = image.get_width()/DEFAULT_TILE_SIZE
		self.height = image.get_height()/DEFAULT_TILE_SIZE

	def get_image(self, filepath_start = "./"):
		""" td.get_image( str ) -> Surface

		Use the stored image_filepath along with the given filepath start to build a filename and load the image of the entity for this Tiledata.
		"""
		filename = "./images/" + self.image_filepath.split("/")[-1]
		return TileData.load_image(filename)
	
	def get_animation_set(self, tile_size, filepath_start = "./"):
		key = self.image_filepath.split("/")[-1]
		key = key.split(".bmp")[0]
		animation_keys = self.animation_keys()
		image_rect = Rect(0, 0, tile_size*self.width, tile_size*self.height)
		animation_filepath = "./animations"
		default_key = animation_keys[0][0]
		default_animation_filename = key + "_" + default_key + ".bmp"
		default_animation = GameImage.load_animation("./animations", default_animation_filename, image_rect, DEFAULT_COLORKEY)
		animation_set = AnimationSet(default_animation)
		
		for n in xrange(1, len(animation_keys)):
			anim_file_key = animation_keys[n][0]
			anim_key = animation_keys[n][1]
			anim_direction = animation_keys[n][2] 
			anim_frames = 10
			if len(animation_keys[n]) > 3:
				anim_frames = animation_keys[n][3]
			animation_filename = key + "_" + anim_file_key + ".bmp"
			next_animation = GameImage.load_animation(animation_filepath, animation_filename, image_rect, colorkey, True, anim_frames)
			animation_set.insertAnimation(next_animation, anim_direction, anim_key)
		return animation_set

	@staticmethod
	def load_image (filename, alpha = False, colorkey = None):
		""" td.load_image( str, bool, str ) -> Surface

		Load an image from the given filename.
		The alpha arg tells us whether there is any transparency in the image (I think).
		"""
		surface = image.load(filename)
		if colorkey:
			surface.set_colorkey (colorkey)
		if alpha or surface.get_alpha ():
			return surface.convert_alpha ()
		return surface.convert ()

	def category(self):
		""" td.category( ) -> str

		Use a string key for this TileData's specific entity in order to get a more general 
		string key for the type of entity it is. 
		"""
		return ENTITY_CATEGORY_MAP[self.entity_key]

	def is_animated(self):
		""" td.is_animated( ) -> bool

		Find out whether the entity loaded from this tiledata will be animated or not.		
		"""
		return (self.entity_key in ANIMATION_KEY_MAP or 
				self.category() in CATEGORY_ANIMATION_KEY_MAP)

	def animation_filepath(self, filepath_start = "./"): 
		""" td.animation_filepath( str ) -> str

		Build the filepath for this tiledata's associated animation(s).
		"""
		filepath = filepath_start + "animations"
		key = self.entity_key
		if key not in ENTITY_CATEGORY_MAP or key == None: 
			return None
		filepath += "/" + self.category() + "/" + key + "/"
		return filepath

	def animation_keys(self):
		""" td.animation_keys( ) -> [ ( str, str, str ) ]

		Grab the animation string keys associated with this tiledata. These will be used to load animations
		and associate them with different states like "idle" or "walking" alnog with dircetion IDs like "left" and "right"
		"""
		key = self.entity_key
		if key in ANIMATION_KEY_MAP:
			return ANIMATION_KEY_MAP[key]
		if self.category() in CATEGORY_ANIMATION_KEY_MAP:
			return CATEGORY_ANIMATION_KEY_MAP[self.category()]
		return None

	def formatted_data(self):
		""" td.formatted_data( ) -> ( str, str, int, int ) 

		Format this tiledata into primitive types that can be saved to file.
		"""
		return (self.entity_key, self.image_filepath, self.width, self.height) 

class BlockedTileData(TileData): 
	""" BlockedTileData( TileData, int, int ) -> BlockedTileData

	This is a space in a room's tiles blocked out by some object that takes up more than one tile.

	Attributes:

	origin_tile: The upper-left TileData that this TileData's entity is associated with.

	origin_x, origin_y: The location of the origin_tile.
	"""
	def __init__(self, origin_tile, x, y):
		self.origin_tile = origin_tile
		self.origin_x, self.origin_y = x, y

	def formatted_data(self):
		""" btd.formatted_data( ) -> None

		Since the width and height of the origin tile will dictate where blocked tiles will be placed,
		there is no need to specifically save a BlockedTileData to file.
		"""
		return None