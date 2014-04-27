""" A scripted game event, like a sign displaying text or a cutscene.
"""

from dialog import *

class GameEvent:
	def __init__(self, dialogs = []): #TEMP
		self.dialogs = dialogs
		self.current_dialog = None

	def execute(self, level):
		level.begin_event(self)
		if self.dialogs:
			self.current_dialog = self.dialogs[0]
		level.display_dialog(self.current_dialog)

	def continue_event(self):
		return False #TEMP

	#def display_dialog(self, screen, dialog):
	#	dialog.display(screen)
		