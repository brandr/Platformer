""" Organizes various control contexts based on the situation.
"""

from maingamecontrols import * 
from eventcontrols import *

class ControlManager:
	""" ControlManager( ... ) -> ControlManager

	Can hold one Controls object at a time.

	Attributes:

	Controls: current control scheme for keyboard input.

	"""

	def __init__(self, controls):
		self.current_controls = controls
		self.current_controls.control_manager = self
		self.screen = None

	def process_event(self, event):
		self.current_controls.process_event(event)

	def switch_screen(self, screen):
		self.screen.switch_screen(screen)

	def switch_controls(self, controls):
		controls.control_manager = self
		self.current_controls = controls #not sure if this will work

	def switch_to_main_controls(self, player):
		main_controls = MainGameControls(player)
		self.switch_controls(main_controls)

	def switch_to_event_controls(self, event, player):
		event_controls = EventControls(event, player)
		self.switch_controls(event_controls)