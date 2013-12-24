import pygame
from pygame import *

BLACK = Color("#000000")
WHITE = Color("#FFFFFF")

class GuiComponent(object):

	def __init__(self,x,y,width,height,bg = WHITE,image = None):
		self.x,self.y = x,y
		self.width,self.height = width,height
		self.subcomponents = []
		self.image = Surface((width,height))
		self.image.fill(bg)
		if(image != None):
			self.image.blit(image,(0,0))

	def button_at(self,pos):
		for c in self.subcomponents:
			if c.contains(pos):
				relative_pos = c.relative_pos(pos)
				return c.button_at(relative_pos)
		return None

	def insert(self,subcomponent):
		self.subcomponents.append(subcomponent)
		pos = (subcomponent.x,subcomponent.y)
		#self.image.blit(subcomponent.image,pos)

	def update(self):
		for c in self.subcomponents:
			c.update()
			self.image.blit(c.image,(c.x,c.y))

	def contains(self,pos):
		return (self.x <= pos[0] <= self.x+self.width and self.y <= pos[1] <=self.y+self.height)

	def relative_pos(self,pos):
		return (pos[0]-self.x,pos[1]-self.y)