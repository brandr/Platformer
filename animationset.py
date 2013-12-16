import spritestripanimator
from spritestripanimator import *

class AnimationSet(object):
	def __init__(self, default_animation = None):
		self.animations = {}
		if(default_animation != None):
			self.insertAnimation(default_animation,'default','default')

	def set_in_direction(self,direction): #could also make direction a tuplet like (0,1) and organize spriteSheets accordingly
		if(direction == None):
			return None
		return self.animations[direction]

	def insertAnimation(self, animation,direction,ID = 'idle'): #"default" might be a better default ID
		if (not direction in self.animations.keys()): 
			self.animations[direction] = {}
		self.animations[direction][ID] = animation

	def default_animation(self):
		if (not 'default' in self.animations.keys()
			or not 'default' in self.animations['default'].keys()): #if direciton is replaced with coords, replace default with (0,0)
			return None
		return self.animations['default']['default']