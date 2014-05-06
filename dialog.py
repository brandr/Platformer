""" An ingame dialog, as from a sign or a character.
"""

from pygame import font, Color, Surface
#from pygame.font import *
from effect import *

BLACK = Color("#000000") #TEMP
WHITE = Color("#FFFFFF")

SIGN = "sign"
SCROLL_CONSTANT = 2.5

class Dialog(Effect):
	def __init__(self, source, text = "", dimensions = (0, 0), scrolling = False, font_color = BLACK): #TODO: consider an arg just for the font.
		Effect.__init__(self, Dialog.draw_image)
		self.next_actions = []
		self.index = 0
		self.draw_pane = None
		if source in PANE_MAP:
			self.draw_pane = PANE_MAP[source]
		self.text = text
		self.dimensions = dimensions
		self.scrolling = scrolling
		self.font_color = font_color
		self.offset = (12, 12) #TEMP

	def draw_text_image(self):
		current_text = self.text[0:int(self.index/SCROLL_CONSTANT)] #TODO: get a number of letters dependent on index
		text_font = font.Font("./fonts/FreeSansBold.ttf", 20)	#TEMP
		text_image = text_font.render(current_text, 1, self.font_color)
		text_image.convert()
		return text_image

	def draw_image(self, level):
		pane_image = self.draw_pane(self)
		text_image = self.draw_text_image()	#TEMP. may be different if signs have scrolling text.
		sign_image = pane_image
		sign_image.blit(text_image, (0, 0))
		return sign_image, (0, 0)

	def sign_pane_image(self):
		pane = Surface(self.dimensions) #TEMP. make it cuter.
		pane.fill(WHITE)
		return pane

	#even though dialog inherits from effect, it shares some methods with GameAction.

	def add_next_action(self, action):
		self.next_actions.append(action)

	def continue_action(self, event, level):
		if(self.index/SCROLL_CONSTANT <= len(self.text)):
			self.index = int(SCROLL_CONSTANT * len(self.text))
			return True
		event.remove_action(self)
		if self.next_actions:
			level.remove_effect(self)
			for a in self.next_actions:
				event.add_action(a)
				a.execute(level)
			return True
		return False

	def execute(self, level):
		level.display_dialog(self)

	def update(self):
		self.index += 1

PANE_MAP = {
	SIGN:Dialog.sign_pane_image
}

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