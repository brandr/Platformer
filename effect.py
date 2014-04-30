""" A visual effect that appears in the game, like a dialog box or black cutscene bars.
"""

from pygame import *

class Effect:
	""" Effect( ... ) -> Effect

	TODO
	"""

	def __init__(self, draw_function, draw_dimensions = (0, 0), offset = (0, 0)): #TODO: provide method or information needed to create the Surface we want, since we don't want to save a Surface every time we make an Effect.
		self.draw_function = draw_function
		self.draw_dimensions = draw_dimensions
		self.offset = offset

	def draw_black_rectangle(self, dimensions, arg = None):
		return Surface(dimensions)

	def draw_image(self):
		return self.draw_function(self, self.draw_dimensions)