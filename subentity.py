"""An entity linked to (and usually dependent upon) another entity.
"""

from being import *

LEFT = 'left'
RIGHT = 'right'

class SubEntity(Being): #NOTE: should lanterns be a subentity?
	""" TODO: docstring
	"""
	def __init__(self, superentity, animations, x = None, y = None):
		self.superentity = superentity
		Being.__init__(self, animations, x, y)
		self.animated = True
		self.active = False
		self.active_count = 0
		self.follow_offset = (0, 0)

	def activate(self):
		if self.active: return
		self.active = True
		self.superentity.add_subentity(self)

	def deactivate(self):
		self.active = False
		self.superentity.remove_subentity(self)

	def update(self):
		GameImage.updateAnimation(self, 256)
		self.check_collisions()
	
	#TODO: consider checking collisions in a general way if subentities have enough commonality.
	#for instance, many (but not all) subentities may copy Being's collide method for platforms.
	#def check_collisions(self):
	#	level = self.superentity.currrent_level
	def check_collisions(self):
		pass

	def single_animation_update(self):
		if self.active and self.animation.at_end():
			self.deactivate()

	def timed_update(self):
		if self.active:
			self.active_count -= 1
			if self.active_count <= 0:
				self.deactivate()

	def follow_update(self):
		if self.active:
			coords = self.superentity.rect_coords()
			self.moveRect(self.follow_offset[0] + coords[0], self.follow_offset[1] + coords[1], True)