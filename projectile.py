""" A projectile that flies through the air and damages some things that it hits.
"""

from being import Being
import pygame 

class Projectile(Being):
	""" Projectile( AnimationSet, int, int ) -> Projectile

	A projectile is somewhat like a subentity in that its behavior depends somewhat on the one who lauched it.
	It may disappear when it hits a viable target, when it hits an obstacle, when the being that launched it is destroyed, or some combination of the above.
	It always disappears when it leaves the level, however.
	"""
	def __init__(self, superentity, animations, x, y, xvel, yvel):
		Being.__init__(self, animations)
		self.animated = True
		self.superentity = superentity
		self.rect.centerx, self.rect.centery = x, y
		self.xvel, self.yvel = xvel, yvel
		self.damage = 1
		self.destroy_key = None
		self.destroying = False

	def destroy(self):
		""" p.destroy( ) -> None

		The projectile is destroyed and removed from the level.
		Note that this is to be called after any "destruction" animations.
		"""
		self.superentity.current_level.remove(self)
		self.superentity.active_projectiles.remove(self)

	def collide(self, other):
		""" p.collide( Entity ) -> None

		The projectile collides with some target.
		Not yet sure if/how blocks should stop projectiles.
		"""

	def update(self):
		""" p.update( ) -> None

		The projectile follows whatever movement behavior is associated with it.
		"""
		self.updateAnimation()
		if self.destroying:
			self.destroy_update()
			return
		self.position_update()
		self.collision_update()
		self.exit_level_check()

	def position_update(self):
		""" p.position_update( ) -> None

		Updates the projectile's position based on its x and y velocity.
		May implement acceleration at some point, too.
		"""
		self.rect.left += self.xvel
		self.rect.top += self.yvel

	def collision_update(self):
		""" p.collision_update( ) -> None

		Check for all collisions with monsters/the player.
		Still not sure if all projectiles should be blocked by impassables.
		"""
		level = self.current_level
		hittables = level.getMonsters()
		hittables.append(level.getPlayer())
		impassables = level.get_impassables()

		# try to figure out where armor checks go

		for i in impassables:
			if pygame.sprite.collide_rect(self, i):
				self.mask = pygame.mask.from_surface(self.image)
				i.mask = pygame.mask.from_surface(i.image)
				if pygame.sprite.collide_mask(self, i):
					self.begin_destroy("plink")
					return

		for h in hittables:
			if not h == self.superentity and pygame.sprite.collide_rect(self, h):
				if self.armor_collide(h): return
				self.mask = pygame.mask.from_surface(self.image)
				h.mask = pygame.mask.from_surface(h.image)
				if pygame.sprite.collide_mask(self, h):
					h.bounceAgainst(self)
					h.take_damage(self.damage)
					self.begin_destroy("hit")
					return

	def armor_collide(self, other):
		""" p.armor_collide( Being ) -> None

		Check to see if the projectile is hitting the other's armor.
		"""
		for a in other.armor_set:
			self.mask = pygame.mask.from_surface(self.image)
			a.mask = pygame.mask.from_surface(a.image)
			if pygame.sprite.collide_mask(self, a):
				self.begin_destroy("plink")
				return True
		return False

	def destroy_update(self):
		""" p.destroy_update( ) -> None

		Update to be called as the projectile is being destroyed.
		"""
		if self.animation.at_end(): self.destroy()

	def begin_destroy(self, key):
		""" p.begin_destroy( str ) -> None

		Begin destroying the projectile using the given string.
		"""
		self.destroy_key = key
		self.destroying = True
		self.xvel, self.yvel = 0, 0
		self.changeAnimation(key, self.direction_id)

	def exit_level_check(self):
		""" p.exit_level_check( ) -> None

		If the projectile is outside the level, it is destroyed.
		Note that this might not always be what we want, as in the case of a homing projectile.
		"""
		dimensions = self.current_level.get_dimensions()
		pixel_width, pixel_height = dimensions[0]*32, dimensions[1]*32
		if self.rect.right < 0 or self.rect.left > pixel_width or self.rect.bottom < 0 or self.rect.top > pixel_height:
			self.destroy()

	#TODO: damage enemies, but not whoever lauched the projectile.