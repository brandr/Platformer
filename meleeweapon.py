""" A melee weapon that is swung and made active (able to hit enemies) and can cause damage.
"""

from entityeffect import *

class MeleeWeapon(SubEntity):
	""" TODO: docstring
	"""
	def __init__(self, superentity):
		#TODO: animation set
		animation_set = None #TODO: actually build the animation set or take it as an arg (maybe use a WeaponFactory?)
		SubEntity.__init__(self, superentity, animation_set)