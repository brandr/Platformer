""" A ladder that the player (and maybe monsters) can climb up or down.
"""

from block import *

class Ladder(Block):
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.is_solid = False

	#TODO: map ladders properly in darkness