""" A subentity that only exists as a visual effect.
"""

from subentity import *

class EntityEffect(SubEntity):
	""" TODO: docstring """

	def __init__(self, superentity, animations, x = None, y = None):
		SubEntity.__init__(self, superentity, animations, x, y)

	def update(self):
		self.animate()
		if self.animation.at_end():
			self.superentity.remove_entity_effect(self)