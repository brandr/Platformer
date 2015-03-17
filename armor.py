""" Some sort of plating that protects the wearer from attacks.
"""

from animationset import AnimationSet
from entityeffect import EntityEffect
from subentity import SubEntity, LEFT, RIGHT
from gameimage import GameImage

import pygame
from pygame import Rect

class Armor(SubEntity):
	""" Armor( Entity, AnimationSet ) -> Armor

	A piece of armor that belongs to some superentity.
	An attack that hits this armor will not harm the superentity.

	Attributes:
	TODO
	"""
	def __init__(self, superentity, animation_set):
		SubEntity.__init__(self, superentity, animation_set)
		self.default_image = self.animation.images[0]
		#TODO: armor characteristics
		#self.damage = 1 #TEMP

	def activate(self, off_x = 0, off_y = 0, direction_id = RIGHT):
		""" a.activate( int, int, str ) -> None

		Make the armor start appearing onscreen.
		"""
		if self.active: return
		self.direction_id = direction_id
		if direction_id == 'left': off_x *= -1
		self.changeAnimation('idle', direction_id)
		SubEntity.activate(self, True)
		self.follow_offset = (off_x, off_y)
		coords = self.superentity.rect_coords()
		x, y = coords[0] + off_x, coords[1] + off_y
		self.moveRect(x, y, True)

	def update(self):
		""" a.update( ) -> None

		Performs the basic updates associated with SubEntities.
		Note that it does not perform the "single animation update",
		because armor does not vanish after completing an animation.
		"""
		self.changeAnimation('idle', self.superentity.direction_id)
		SubEntity.update(self)
		SubEntity.follow_update(self)

	def block_attack(self, damage_source):
		""" a.block_attack( ? ) -> bool

		Returns true if the armor blocks the attack and false if it does not.
		May also destroy the armor.
		"""
		#if armor is breakable, deal with it here
		return True #TODO