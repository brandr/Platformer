""" A factory for generating armors, which will probably only be used by monsters.
"""

from pygame import image, Rect 

from gameimage import GameImage
from animationset import AnimationSet
from armor import Armor

def armor_animation_set(animation_data):
	""" armor_animation_set( ( Rect, [ ( str, str, str ) ] ) ) -> AnimationSet

	Returns an animationset for an armor based on a rect and a list of string key tuplets of the form:
	(filename, direction key, state key).
	"""
	filepath = './animations/'
	armor_rect =  animation_data[0]
	animation_set_data = animation_data[1]
	default_anim_data = animation_set_data[0]
	default_animation = GameImage.load_animation(filepath, default_anim_data[0], armor_rect, -1, True, 10) #last 2 args are temp
	animation_set = AnimationSet(default_animation)
	for d in animation_set_data:
		filename = d[0]
		animation = GameImage.load_animation(filepath, filename, armor_rect, -1, True, 10) #last 2 args are temp
		animation_set.insertAnimation(animation, d[1], d[2])
	return animation_set

def build_armor(armor_key, superentity):
	""" build_armor( str, Being ) -> Armor

	Builds an armor with the correct properties
	Will become more sophisticated as more armor types are added.
	"""
	animation_data = ARMOR_ANIMATION_DATA_MAP[armor_key]
	animation_set = armor_animation_set(animation_data)
	return Armor(superentity, animation_set)

LEFT = "left"
RIGHT = "right"

IDLE = "idle"
#SWINGING = "swinging"

#SWORD = "sword"
#PICK = "pick"
FROG_MASK = "frog_mask"

ARMOR_ANIMATION_DATA_MAP = {
	FROG_MASK:
		(
		Rect(0, 0, 64, 64),
			[
			("frog_mask_idle_left.bmp", LEFT, IDLE),
			("frog_mask_idle_right.bmp", RIGHT, IDLE)
			]
		)
}