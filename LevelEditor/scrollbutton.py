import button
from button import *

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

class ScrollButton(Button):
	def __init__(self,image,greyed_image,scroll_pane,direction,x,y,magnitude = 16):
		effect_args = direction,magnitude
		Button.__init__(self,image,x,y,scroll_pane.scroll,*effect_args)
		self.scroll_pane = scroll_pane
		self.direction = direction
		self.magnitude = magnitude
		self.normal_image = image
		self.greyed_image = greyed_image

		#TODO: if it helps, consider greying out the button when there is no more room to scroll up or down.
	def update(self,scroll_x,scroll_y):
		#print "UPDATING"
		if(self.direction[0] != 0):
			if (scroll_x):
				self.image = self.normal_image
			else:
				self.image = self.greyed_image
			return
		if(self.direction[1] != 0):
			if (scroll_y):
				self.image = self.normal_image
			else:
				self.image = self.greyed_image
			return