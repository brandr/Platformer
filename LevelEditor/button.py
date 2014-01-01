#TODO: imports
import pygame
from pygame import *
#import guicomponent
#from guicomponent import *
#a button is an object with a position defined by x and y, and it can be interacted with via
	#the mouse.
BLACK = Color("#000000")
WHITE = Color("#FFFFFF")
LEFT_MOUSE = 1

class Button(object):
	#TODO: consider making this inherit from guicomponent.
	#TODO: consider making effects and their args arrays, rather than single fuctions.
	def __init__(self,image,x,y,effect,*effect_args):
		self.image = image
		self.image.convert()
		self.x,self.y = x,y
		self.effect = effect
		self.effect_args = effect_args
		#print self.effect_args

	def update(self):
		pass

	def contains(self,pos):
		return (self.x <= pos[0] <= self.x+self.width() and self.y <= pos[1] <=self.y+self.height())

 #TODO: in the actual editor, this will depend on the type of button.
  		#There will likely be different button subclasses which override this method.
	def processClick(self,down,mouse_button): #TODO: consider different effects for pressing and releasing, left and right mousebuttons, etc
		if self.effect != None and down and mouse_button == LEFT_MOUSE:
			self.effect(*(self.effect_args))

	def addText(self,text_string,font_size,x,y):
		text = Button.text_component(text_string,font_size,BLACK)#,(x,y))
		self.image.blit(text,(x,y))

	@staticmethod
	def text_component(text_string,font_size,color):#,color,offset):
		font = pygame.font.Font(None, font_size)
		return font.render(text_string, 1, color)
		#width = text.get_rect().width
		#height = text.get_rect().height
		#return GuiComponent(offset[0],offset[1],width,height,WHITE,text)

	def width(self):
		return self.image.get_width()

	def height(self):
		return self.image.get_height()