import pygame
from pygame import *
import button
from button import *

#BLACK = Color("#000000")
#WHITE = Color("#FFFFFF")
DEFAULT_MARGIN = 32

class GuiComponent(object):

	def __init__(self,x,y,width,height,bg = WHITE,image = None):
		self.x,self.y = x,y
		self.width,self.height = width,height
		self.subcomponents = []
		self.bg = bg
		self.image = Surface((width,height))
		self.image.fill(bg)
		if(image != None):
			self.image.blit(image,(0,0))

	def button_at(self,pos):
		for c in self.subcomponents:
			if c.contains(pos):
				if isinstance(c,Button):
					return c
				relative_pos = c.relative_pos(pos)
				return c.button_at(relative_pos)
		#TODO: consider allowing the stadard guicomponent to have buttons on it.
		return None

	def insert(self,subcomponent):
		self.subcomponents.append(subcomponent)
		pos = (subcomponent.x,subcomponent.y)

	def update(self):
		for c in self.subcomponents:
			c.update()
			self.image.blit(c.image,(c.x,c.y))

	def get_window_at(self,x,y,width,height):
		window = Surface((width,height))
		window.blit(self.image,(-x,-y))
		return window

	def contains(self,pos):
		return (self.x <= pos[0] <= self.x+self.width and self.y <= pos[1] <=self.y+self.height)

	def relative_pos(self,pos):
		return (pos[0]-self.x,pos[1]-self.y)

	def addText(self,text_string,font_size,x,y):
		text = GuiComponent.text_component(text_string,font_size,BLACK,(x,y))
		self.insert(text)

	@staticmethod
	def text_component(text,font_size,color,offset):
		font = pygame.font.Font(None, font_size)
		text = font.render(text, 1, color)
		width = text.get_rect().width
		height = text.get_rect().height
		return GuiComponent(offset[0],offset[1],width,height,WHITE,text)