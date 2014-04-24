""" A sign that the player can read. No one else can, though.
"""

from block import *

class Sign(Block):
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False