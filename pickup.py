""" An abstract class for things that the player can pick up/absorb by touching.
"""

from entity import *

class Pickup(Entity):
	""" Pickup( ... ) -> Pickup

	attributes:
	TODO
	"""
	def __init__(self, animations, x, y):
		Entity.__init__(self, animations)
		self.rect.centerx += x
		self.rect.centery += y

	def take_effect(self, player):
		pass

class OilPickup(Pickup):
	""" OilPickup( ... ) -> OilPickup

	attributes:
	TODO
	"""
	def __init__(self, animations, x, y):
		Pickup.__init__(self, animations, x, y)
		self.oil_value = 1000 #TEMP. consider allowing it to be changed in the leveleditor

	def take_effect(self, player):
		if player.get_lantern():
			player.get_lantern().add_oil(self.oil_value)
