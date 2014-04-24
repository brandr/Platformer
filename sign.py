""" A sign that the player can read. No one else can, though.
"""

from block import *
from gameevent import *

class Sign(Block):
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.text = "This is the only thing any sign can ever say." #TODO: once signs work, figure out how their text should be set.
		dialog = Dialog(self.text)
		self.event = GameEvent([dialog]) #TEMP

	def execute_event(self, level):
		self.event.execute(level) #TEMP