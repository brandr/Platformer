""" A factory for creating items.
"""

from pygame import image, Rect 

from gameimage import GameImage
from animationset import AnimationSet
from chestcontents import SUBENTITY_LIST
from weaponfactory import SWINGING

def item_animation_set( animation_data ):
	""" item_animation_set( ( Rect, [ ( str, str, str ) ] ) ) -> AnimationSet

	Returns an animationset for an item based on a rect and a list of string key tuplets of the form:
	(filename, direction key, state key).
	"""
	filepath = './animations/'
	item_rect =  animation_data[0]
	animation_set_data = animation_data[1]
	default_anim_data = animation_set_data[0]
	default_animation = GameImage.load_animation(filepath, default_anim_data[0], item_rect, -1, True, 10) #last 2 args are temp
	animation_set = AnimationSet( default_animation )
	for d in animation_set_data:
		filename = d[0]
		animation = GameImage.load_animation(filepath, filename, item_rect, -1, True, 10) #last 2 args are temp
		animation_set.insertAnimation( animation, d[1], d[2] )
	return animation_set

def build_item( constructor, key, x, y ):
	""" build_item( str,  ) -> Item

	Builds an item using the given constructor, string key (for fetching necessary data), and coordinates.
	Coordinates may be useful if this method is used to create blocks while the game is running, but I'm not sure.
	"""
	animation_data = ITEM_ANIMATION_DATA_MAP[key]
	animation_set = item_animation_set(animation_data)
	item = None
	if key in SUBENTITY_LIST: item = constructor(None, animation_set) #TMP
	else: item = constructor( animation_set, x, y )
	# TODO: additional init  methods go here. (may need to take more args)
	return item

DEFAULT = "default"
IDLE = "idle"
LEFT = "left"
RIGHT = "right"

LANTERN = "lantern"
SWORD = "sword"

ITEM_ANIMATION_DATA_MAP = {
	LANTERN:
		(
			Rect(0, 0, 32, 64),
			[
				( "lantern_idle_left.bmp", DEFAULT, DEFAULT ),
				( "lantern_idle_left.bmp", LEFT, IDLE ),
				( "lantern_idle_right.bmp", RIGHT, IDLE ),
			]	
		),
	SWORD:
		(
			Rect(0, 0, 32, 32),
			[
				("test_sword_1_swinging_left.bmp", DEFAULT, DEFAULT),
				("test_sword_1_swinging_left.bmp", LEFT, SWINGING),
				("test_sword_1_swinging_right.bmp", RIGHT, SWINGING)
			]
		)
}