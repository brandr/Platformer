""" A cutscene during which things happen and buttons only advance the dialog.
"""

from gameevent import *

class Cutscene(GameEvent):
	""" TODO: docstring
	"""
	def __init__(self, start_actions = []): #TODO: figure out what is special about cutscenes that can be used to separate them from normal events
		GameEvent.__init__(self, start_actions)
		self.level = None #TODO: either make a way to set level, or create a system that doesn't need it.
		#self.duration = 60 #TEMP. Later, we want to give each action in the cutscene a duration instead.

	def begin(self):
		for a in self.current_actions:
			a.execute(self.level) #TODO: activate all start actions.
		#self.actions[0].right = True #TEMP. Make this more general, and also make it possible for the cutscene to progress/end.

	def update(self, level):
		for a in self.current_actions:
			a.update(self)
	
	def continue_event(self): #TODO: change this method if pressing buttons should affect cutscenes.
		return True

	#def is_complete(self):
	#	return not self.current_actions
		#return self.duration <= 0 #TEMP