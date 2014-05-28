""" A door that the player can open, often hiding a monster or treasure.
"""

from block import *

class Door(Block): #not sure how to handle a 2-part block yet
	"""TODO: docstring"""
	def __init__(self, animations, x, y):
		#TODO: build open and closed images out of input
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.is_solid = True
		self.x_interactable = True
		self.open = False
		self.open_door_image = None

	def in_interact_range(self, player):
		return True #TEMP: check distance first

	def execute_x_action(self, level, player):
		if not self.open: self.set_open()

	def set_open(self):
		self.default_image = self.open_door_image
		self.image = self.open_door_image
		self.is_solid = False
		self.is_square = True

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