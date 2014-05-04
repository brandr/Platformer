""" Handles the controls used during a cutscene, while reading a sign, etc.
"""

from controls import *

class EventControls(Controls):
	""" EventControls( Event ) -> EventControls

	Can handle various contexts related to events.

	Attributes:

	Event: the event associated with these controls. 
	"""

	def __init__(self, event, player):
		Controls.__init__(self)
		self.event, self.player = event, player
		self.initialize_control_map(EVENT_CONTROL_MAP) #TEMP. control map might vary based on the particular event.

	def prompt_continue_event(self, key, toggle):	#TODO: this should send information to the event which will do nothing if it is a cutscene but advance the event if it is dialogue.
		if(toggle and not self.event.continue_event()):
			self.end_event()

	def end_event(self):
		self.player.current_level.clear_effects()
		self.control_manager.switch_to_main_controls(self.player)

prompt_continue_event = EventControls.prompt_continue_event
EVENT_CONTROL_MAP = {
	K_x:prompt_continue_event
}