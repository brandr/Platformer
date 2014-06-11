""" A sword that the player can swing. Find a general class to describe this object in the long run.
"""

from subentity import *

from pygame import image #TEMP (give this to factory later, maybe)

class Sword(SubEntity): #TODO: different inheritance system (maybe add an intermediate "weapon" class and make sword not its own class?)
	""" TODO: docstring """
	
	#TODO: implement:
	# -swinging animation
	# -swinging direction
	# -collisions with other objects (like monsters)
	# -damage

	def __init__(self, player):

		sword_anim_set = Sword.load_sword_animation_set()

		#TEMP
		surface = image.load('./images/test_sword_right.bmp')
		sword_image = surface.convert ()
		#sword_animations = GameImage.still_animation_set(sword_image, Rect(0, 0, 32, 16))
		SubEntity.__init__(self, player, sword_anim_set)
		self.default_image = self.animation.images[0]
		#TEMP

	@staticmethod
	def load_sword_animation_set(): # look for a more general way to do this
		sword_rect = Rect(0, 0, 32, 32)
		filepath = './animations/'

		sword_swinging_right = GameImage.load_animation(filepath, 'test_sword_swinging_right.bmp', sword_rect, -1)
		sword_swinging_left = GameImage.load_animation(filepath, 'test_sword_swinging_left.bmp', sword_rect, -1)	#TODO: add left swing animation

		animation_set = AnimationSet(sword_swinging_right)
		animation_set.insertAnimation(sword_swinging_right, 'right', 'swinging')
		animation_set.insertAnimation(sword_swinging_left, 'left', 'swinging')

		return animation_set

	def activate(self, off_x = 0, off_y = 0, direction_id = RIGHT):

		#TODO: 
		# 1. make the sword animated with a swinging animation
		# 2. pass direction_id into the SubEntity activate method
		# 3. change where off_x is positive or negative based on L/R direction.
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

	def update(self):
		SubEntity.update(self)
		#SubEntity.timed_update(self)
		SubEntity.single_animation_update(self)
		SubEntity.follow_update(self)