""" A special factory for making doors.
"""

from door import *

class DoorFactory:
	""" TODO: docstring
	"""
	@staticmethod
	def build_entity(raw_door_image, door_rect, door_data, x, y):	
		door_width, door_height = raw_door_image.get_width()/2, raw_door_image.get_height()
		door_rect = Rect(door_rect.left, door_rect.top, door_rect.width/2, door_rect.height)
		closed_door_image = raw_door_image.subsurface(Rect(0, 0, door_width, door_height))
		open_door_image = raw_door_image.subsurface(Rect(door_width, 0, door_width, door_height))
		door_anim_set = GameImage.still_animation_set(closed_door_image, door_rect)
		door = Door(door_anim_set, x, y)
		door.open_door_image = open_door_image
		return door