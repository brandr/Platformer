"""A visible object that may overlap any object on a level. Has no effect but may lead the player towards some places.
"""

from gameimage import GameImage
from pygame import Rect

class LevelEffect(GameImage):
	""" LevelEffect( AnimationSet, int, int ) -> LevelEffect

	A LevelEffect is usually partially transparent, usually animated, and never directly affects gameplay.
	"""
	def __init__(self, animations, x, y):
		GameImage.__init__(self, animations)
		self.rect = Rect(x, y, 32, 32) # not sure about these dimensions
		self.animated = True

	def update(self):
		self.updateAnimation()