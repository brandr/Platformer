#TODO: imports
import pygame
from pygame import *
#a button is an object with a position defined by x and y, and it can be interacted with via
	#the mouse.
class Button(object):

	BLACK = Color("#000000")
	WHITE = Color("#FFFFFF")

	def __init__(self,image,x,y):
		self.image = image
		self.x,self.y = x,y

	def update(self):
		pass