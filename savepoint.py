from entity import Entity
from pygame import Rect

class SavePoint(Entity):
	""" SavePoint( AnimationSet, int, int ) -> SavePoint

	A SavePoint is a special entity that allows the player to save the game.
	It will probably be easiest to make it work similarly to an NPC or a sign, since it will open a dialog

	Attributes:

	"""
	def __init__(self, animations, x, y):
		Entity.__init__(self, animations)
		self.rect = Rect(x, y, 32, 32)