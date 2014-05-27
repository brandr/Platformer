""" A door that the player can open, often hiding a monster or treasure.
"""

from block import *

class Door(Block): #not sure how to handle a 2-part block yet
	"""TODO: docstring"""
	def __init__(self, animations, x, y):
		#TODO: build door blocks
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.is_solid = True

	def additional_block(self, x, y):
		door_component_image = self.image #TEMP
		door_component_rect = Rect(0, 0, 32, 32)
		door_animation_set = GameImage.still_animation_set(door_component_image, door_component_rect)
		return DoorBlock(door_animation_set, x, y)

	def fill_tiles(self, tiles):
		width, height = self.tile_dimensions()
		coords = self.coordinates()
		for y in range(coords[1], coords[1] + height):
			for x in xrange(coords[0], coords[0] + width):
				tiles[y][x].block = self #TEMP: should probably generate doorblock here

class DoorBlock(Block):
	""" TODO: docstring"""
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)