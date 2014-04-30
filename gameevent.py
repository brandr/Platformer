""" A scripted game event, like a sign displaying text or a cutscene.
"""

from dialog import *

class GameEvent:
	def __init__(self, actions = []): #TEMP
		self.actions = actions
		self.current_dialog = None

	def execute(self, level):
		level.begin_event(self)
		if self.actions:
			self.current_dialog = self.actions[0] #TEMP: should remain agnostic to dialog/other actions.
		level.display_dialog(self.current_dialog)

	def continue_event(self):
		return False #TEMP. should advance to next action in actions.

	def update(self):
		pass #TODO (or maybe have subclasses inherit)

	def is_complete(self):
		return False #TEMP