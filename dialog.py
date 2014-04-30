""" An ingame dialog, as from a sign or a character.
"""

from pygame import font, Color, Surface
from effect import *

BLACK = Color("#000000") #TEMP

class Dialog(Effect):
	def __init__(self, text = "", font_color = BLACK): #TODO: consider an arg just for the font.
		Effect.__init__(self, Dialog.draw_image)
		self.text = text
		self.font_color = font_color
		self.text_image = None
		self.offset = (12, 12) #TEMP
		#self.font = pygame.font.Font(None, 30)	#TEMP

	def init_text_image(self):
		text_font = font.Font(None, 30)	#TEMP
		text_image = text_font.render(self.text, 1, self.font_color)
		text_image.convert()
		self.text_image = text_image

	def draw_image(self):
		self.init_text_image()
		return self.text_image

	#def display(self, level):
	#	screen = level.screen
	#	text_font = font.Font(None, 30)	#TEMP
	#	text_image = text_font.render(self.text, 1, self.font_color)
		#text_image = Surface((50, 50))
	#	text_image.convert()

	#	screen.blit(text_image, (16, 16))

#TODO: finish making signs.
#TODO: set up screen layer system. 
#TODO: set up controls system based on roguelikeself