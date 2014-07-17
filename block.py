""" An entitty that is "locked" to a tile, like a platform. A tile can only have one block.
"""

from entity import *
	
class Block(Entity):
	""" Block( AnimationSet, int, int ) -> Block

	A Block is more specific than an Entity but less specific than a Platform. I can't think of any blocks that should be able to move.

	Attributes:

	is_sloped: determines whether the block is sloped, affecting how entities will collide with it.
	is_square: determines whether the block is square, affecting collisions and how light will land on it.
	is_solid: determines whether entities can pass through this block.
	"""
	def __init__(self, animations, x, y):
		Entity.__init__(self, animations)
		self.unseen_color = Color("#FFFFFF") #TODO: need "unseen image" instead
		self.rect = Rect(x, y, 32, 32)
		self.is_sloped = False
		self.is_square = True
		self.is_solid = True

	def updateimage(self, lightvalue = 0): 
		""" b.updateimage( int ) -> None

		This method may be outdated with the new lighting system. Consider removing the lightvalue arg.
		"""
		if(lightvalue != 0): 
			self.image = self.default_image 
			self.image.set_alpha(lightvalue)
		else: 
			self.image = Surface((32, 32)) #TODO: consider making the unseen image a const value that 
			if(self.mapped):    #both platforms and tiles can access (or private data if it should vary)
				self.image.fill(self.unseen_color)    #same for unseen color
				self.image.set_alpha(16)
				return
			self.image.fill(BACKGROUND_COLOR)

	def additional_block(self, x, y):
		""" b.additional_block( int, int ) -> None

		I'm not sure if this method is still used or what it was for. Try to find it somewhere else in classes like LevelFactory.
		"""
		return None

	def map(self):
		""" b.map( ) -> None

		Mark that the player has seen this block, causing it to be visible as a grey square in complete darkness.
		"""
		self.mapped = True
		self.unseen_image = self.mapped_block_image()

	def mapped_block_image(self):
		""" b.mapped_block_image( ) -> Surface

		Returns a square image representing the default appearance of the block when the player has seen it but no light is hitting it.
		"""
		block_image = Surface((32, 32))
		self.unseen_color = Color("#000000")
		block_image.fill(self.unseen_color)
		return block_image