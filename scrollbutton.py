import button
from button import *

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

class ScrollButton(Button):
	def __init__(self,image,scroll_pane,direction,x,y,magnitude = 16):
		Button.__init__(self,image,x,y)
		self.scroll_pane = scroll_pane
		self.direction = direction
		self.magnitude = magnitude


	def processClick(self,down,mouse_button): #"down" refers to mouse button going down, not the direction DOWN.
		if(down and mouse_button == LEFT_MOUSE):	
			self.scroll_pane.scroll(self.direction,self.magnitude)