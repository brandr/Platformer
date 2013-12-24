#TODO: imports
import pygame
from pygame import *
#a button is an object with a position defined by x and y, and it can be interacted with via
	#the mouse.
LEFT = 1

class Button(object):

	BLACK = Color("#000000")
	WHITE = Color("#FFFFFF")

	def __init__(self,image,x,y):
		self.image = image
		self.x,self.y = x,y

	def update(self):
		pass
 #TODO: in the actual editor, this will depend on the type of button. There will likely be different buttons which override this method.
	def processClick(self,down,mouse_button):
		if(down and mouse_button == LEFT):	#TEMPORARY FOR TESTING
			self.image.fill(Color("#BB0000"))