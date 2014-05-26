from block import *

class Platform(Block):
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_solid = True

	def update(self, player):	
		pass

	def darkenTo(self, lightvalue):
		self.image = self.default_image
		current_lightvalue = self.image.get_alpha()
		self.image.set_alpha(min(current_lightvalue, lightvalue))

	def map(self):
		self.mapped = True
		self.unseen_image = self.mapped_block_image()

	def mapped_block_image(self):
		block_image = Surface((32, 32))
		self.unseen_color = Color("#FFFFFF")
		block_image.fill(self.unseen_color)
		return block_image