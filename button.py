#TODO: imports

import guicomponent
from guicomponent import *
#a button is an object with a position defined by x and y, and it can be interacted with via
	#the mouse.
LEFT_MOUSE = 1

class Button(object):
	#TODO: consider making this inherit from guicomponent.
	def __init__(self,image,x,y):
		self.image = image
		self.x,self.y = x,y

	def update(self):
		pass

	def contains(self,pos):
		return (self.x <= pos[0] <= self.x+self.width() and self.y <= pos[1] <=self.y+self.height())

 #TODO: in the actual editor, this will depend on the type of button.
  		#There will likely be different button subclasses which override this method.
	def processClick(self,down,mouse_button):
		if(down and mouse_button == LEFT_MOUSE):	#TEMPORARY FOR TESTING
			self.image.fill(Color("#FF0000"))

	def width(self):
		return self.image.get_width()

	def height(self):
		return self.image.get_height()