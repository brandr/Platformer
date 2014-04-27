""" A manager for various game screens that the player might swich between.
"""

from maingamescreen import *

class ScreenManager:
	""" ScreenManager (...) -> ScreenManager

	TODO
	Attributes:
	
	current_screen: the current screen to be displayed. Only one may display at a time.
	"""

	def __init__(self, master_screen, current_screen, player = None):
		self.master_screen = master_screen
		self.set_current_screen(current_screen)
		self.player = player
		if(player != None):
			player.screen_manager = self

	def set_current_screen(self, screen):
		self.current_screen = screen
		screen.screen_manager = self

	def process_event(self, event):
		self.current_screen.control_manager.process_event(event)

	def update_current_screen(self):
		self.current_screen.update()

	def draw_screen(self):
		self.current_screen.draw_screen(self.master_screen)