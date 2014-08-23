""" A melee weapon that is swung and made active (able to hit enemies) and can cause damage.
"""

from entityeffect import *

class MeleeWeapon(SubEntity):
	""" TODO: docstring
	"""
	def __init__(self, superentity, animation_set):
		SubEntity.__init__(self, superentity, animation_set)
		self.default_image = self.animation.images[0]
		self.damage = 1 #TEMP

	# TEMP, COPIED FROM SWORD vvv

	def activate(self, off_x = 0, off_y = 0, direction_id = RIGHT):

		#TODO: 
		# make a "spark" appear if the sword hits a monster
		#print "SWING"
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
		self.rect = Rect(self.rect.left, self.rect.top, 32, 32)
		level = self.superentity.current_level
		monsters = level.getMonsters()
		for m in monsters:
			if m != self.superentity and pygame.sprite.collide_rect(self, m): #TODO: consider using mask instead
				if m.bounce_count <= 0:
					self.mask = pygame.mask.from_surface(self.image)
					m.mask = pygame.mask.from_surface(m.image)
					if pygame.sprite.collide_mask(self, m):
						self.collide_with_monster(m)
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