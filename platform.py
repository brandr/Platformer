""" A platfrom is a block that is solid and obstructs the motion of beings.
"""

from block import Block
from pygame import Surface

class Platform(Block):
	""" Platform( AnimationSet, int, int ) -> Platform

	Unlike some other blocks (like ladders), platforms always obstruct movement. Some of them
	can allow passage under certain conditions.

	Attributes:

	is_solid: Flags that beings cannot pass through the platform
	"""
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_solid = True

	def update(self, player):	
		""" p.update( Player ) -> None

		This is a general method. If a platform should react in some way to the player's prescence, it does so here.
		"""
		pass

	def map(self):
		""" p.map( ) -> None

		Mark that the player has seen this platform.
		"""
		self.mapped = True