""" A melee weapon that is swung and made active (able to hit enemies) and can cause damage.
"""

from animationset import AnimationSet
from entityeffect import EntityEffect
from subentity import SubEntity, LEFT, RIGHT
from gameimage import GameImage

import pygame
from pygame import Rect

class MeleeWeapon(SubEntity):
	""" MeleeWeapon( Entity, AnimationSet ) -> MeleeWeapon

	A weapon that belongs to some superentity and is swung to cause damage.

	Attributes:
	damage: The standard amount of damage that an enemy will take if hit by this weapon.
	"""
	def __init__(self, superentity, animation_set):
		SubEntity.__init__(self, superentity, animation_set)
		self.default_image = self.animation.images[0]
		self.damage = 1 #TEMP
		self.cancelled = False
		self.enemies_hit = []

	# TEMP, COPIED FROM SWORD vvv

	def activate(self, off_x = 0, off_y = 0, direction_id = RIGHT, animation_id = 'swinging'):
		""" mw.activate( int, int, str ) -> None

		The weapon begins swinging.
		This means it will be set to the proper location with respect to its superentity.
		"""
		self.cancelled = False
		self.enemies_hit = []
		self.direction_id = direction_id
		self.animation_id = animation_id
		if direction_id == 'left': off_x *= -1
		self.changeAnimation(animation_id, direction_id)
		SubEntity.activate(self)
		self.follow_offset = (off_x, off_y)
		coords = self.superentity.rect_coords()
		x, y = coords[0] + off_x, coords[1] + off_y
		self.moveRect(x, y, True)
		self.active_count = 20 #TEMP
		self.permanent = False

	def set_idle(self, off_x = 0, off_y = 0, direction_id = RIGHT):
		self.activate(off_x, off_y, direction_id, 'idle')
		self.permanent = True

		#TODO: check for collisions either here or in level class
	def update(self):
		""" mw.update( ) -> None

		Update the weapon's animation and call some subentity update methods.
		"""
		self.changeAnimation(self.animation_id[0], self.direction_id)
		SubEntity.update(self)
		if not self.permanent: SubEntity.single_animation_update(self)
		SubEntity.follow_update(self)
		SubEntity.direction_update(self)

	def check_collisions(self):
		""" mw.check_collisions( ) -> None

		See if the weapon is in contact with anything it can damage.
		Also checks for armor which may block the attack.
		"""
		#TEMP
		# TODO: check things that block collisions with monsters BEFORE checking collisions with monsters
		# This is future robert here. Yes, past robert, I agree with you. In fact, I am just now creating an armor system so thanks very much for the tip!
		# I will later reward you for your loyalty, my pet.
		if self.cancelled: return
		self.rect = Rect(self.rect.left, self.rect.top, 32, 32)		# not sure this is necessary
		targets = self.superentity.hittable_targets()
		if self.superentity in targets: targets.remove(self.superentity)
		for t in targets:
			if not t or t in self.enemies_hit: continue
			self.mask = pygame.mask.from_surface(self.image)
			t.mask = pygame.mask.from_surface(t.image)
			if pygame.sprite.collide_mask(self, t):
				armors = t.armor_set
				for a in armors:
					a.mask = pygame.mask.from_surface(a.image)
					if pygame.sprite.collide_mask(self, a) and a.block_attack(self): 
						a.superentity.bounceAgainst(self.superentity, 15)
						self.cancel_attack()
						return
				if t.bounce_count <= 0:
					self.collide_with_target(t)
					self.enemies_hit.append(t)
					return
		#TEMP

	def collide_with_target(self, target):
		""" mw.collide_with_target( Entity ) -> None

		Called once it is confirmed that this swing damages some entity.
		Deals the appropriate amount of damage and generates a small spark effect.
		"""
		#TODO: the hit spark should be an entityeffect belonging to the player

		relative_hit_coords = pygame.sprite.collide_mask(self, target)
		global_hit_coords = (relative_hit_coords[0] + self.rect.left - 8, relative_hit_coords[1] + self.rect.top - 8)
		hit_spark = self.hit_spark(global_hit_coords)
		self.superentity.add_entity_effect(hit_spark)
		target.collide_with_damage_source(self.superentity)
		target.take_damage(self.damage)

	def cancel_attack(self):
		""" mw.cancel_attack( ) -> None

		Cancels the current swing of this weapon.
		Not yet sure if this is what we want.
		"""
		self.cancelled = True

	def hit_spark(self, coords):
		""" mw.hit_spark( ( int, int ) ) -> EntityEffect

		Returns a visual effect to show that the weapon has struck something.
		"""
		hit_spark_animation = GameImage.load_animation('./animations', 'hit_spark_1.bmp', Rect(0, 0, 16, 16), -1, False, 6)
		hit_spark_animation_set = AnimationSet(hit_spark_animation)
		return EntityEffect(self.superentity, hit_spark_animation_set, coords[0], coords[1])

	def bounceAgainst(self, other):
		""" mw.bounceAgainst( Entity ) -> None

		A method common to other classes in the same hierarchy.
		"""
		return