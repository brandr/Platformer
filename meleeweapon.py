""" A melee weapon that is swung and made active (able to hit enemies) and can cause damage.
"""

from entityeffect import *

class MeleeWeapon(SubEntity):
	""" TODO: docstrings errywhere
	"""
	def __init__(self, superentity, animation_set):
		SubEntity.__init__(self, superentity, animation_set)
		self.default_image = self.animation.images[0]
		self.damage = 1 #TEMP

	# TEMP, COPIED FROM SWORD vvv

	def activate(self, off_x = 0, off_y = 0, direction_id = RIGHT):

		#TODO: 
		# make a "spark" appear if the sword hits a monster
		self.enemies_hit = []
		self.direction_id = direction_id
		if direction_id == 'left': off_x *= -1
		self.changeAnimation('swinging', direction_id)
		SubEntity.activate(self)
		self.follow_offset = (off_x, off_y)
		coords = self.superentity.rect_coords()
		x, y = coords[0] + off_x, coords[1] + off_y
		self.moveRect(x, y, True)
		
		#TODO: start swinging animation
		self.active_count = 24 #TEMP

		#TODO: check for collisions either here or in level class
	def update(self):
		SubEntity.update(self)
		SubEntity.single_animation_update(self)
		SubEntity.follow_update(self)

	def check_collisions(self):
		#TEMP
		# TODO: check things that block collisions with monsters BEFORE checking collisions with monsters
		# TODO: if this weapon belongs to a monster, it can hurt the player. Therfore, instead of level.getMonsters, use some getter for the superentity's enemies.
		self.rect = Rect(self.rect.left, self.rect.top, 32, 32)
		targets = self.superentity.hittable_targets()
		for t in targets:
			if t in self.enemies_hit: continue
			self.mask = pygame.mask.from_surface(self.image)
			t.mask = pygame.mask.from_surface(t.image)
			if pygame.sprite.collide_mask(self, t) and t != self.superentity: #TODO: consider using mask instead
				if t.bounce_count <= 0:
					self.collide_with_monster(t)
					self.enemies_hit.append(t)
					return
		#TEMP

	def collide_with_monster(self, monster):
		
		#TODO: the hit spark should be an entityeffect belonging to the player

		relative_hit_coords = pygame.sprite.collide_mask(self, monster)
		global_hit_coords = (relative_hit_coords[0] + self.rect.left - 8, relative_hit_coords[1] + self.rect.top - 8)
		hit_spark = self.hit_spark(global_hit_coords)
		self.superentity.add_entity_effect(hit_spark)
		
		monster.bounceAgainst(self)
		monster.take_damage(self.damage) #TEMP

	def hit_spark(self, coords):
		hit_spark_animation = GameImage.load_animation('./animations', 'hit_spark_1.bmp', Rect(0, 0, 16, 16), -1, False, 6)
		hit_spark_animation_set = AnimationSet(hit_spark_animation)
		return EntityEffect(self.superentity, hit_spark_animation_set, coords[0], coords[1])