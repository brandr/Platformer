""" A cutscene during which things happen and buttons only advance the dialog.
"""

from gameevent import *

class Cutscene(GameEvent):
	""" Cutscene( [Action] ) -> Cutscene

	A cutscene is a special type of GameEvent which can have somewhat different rules, including a set beginning and end along
	with animations/actions that take set amounts of time.

	Attributes:

	level: the level that the cutscene takes place on.
	"""
	def __init__(self, start_actions = []): #TODO: figure out what is special about cutscenes that can be used to separate them from normal events
		GameEvent.__init__(self, start_actions)
		self.level = None #TODO: either make a way to set level, or create a system that doesn't need it.

	def begin(self):
		""" c.begin( ) -> None

		Activate all start actions for this cutscene.
		"""
		for a in self.current_actions:
			a.execute(self.level) 

	def update(self, level):
		""" c.update( Level ) -> None

		Update all the current ongoing actions for this cutscene.
		"""
		for a in self.current_actions:
			a.update(self)
	
	def continue_event(self): #TODO: change this method if pressing buttons should affect cutscenes. (this may need to be changed once we have cutscenes with dialog)
		""" c.continue_event( ) -> bool

		An abstract method that determines whether this event should continue.
		Other classes handle this method differently.
		"""
		return True