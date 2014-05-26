""" A manager for various game screens that the player might swich between.
"""

from maingamescreen import *
from pausescreen import *

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

	def switch_to_main_screen(self, player):
		game_controls = MainGameControls(player) 
		control_manager = ControlManager(game_controls)
		main_screen = MainGameScreen(control_manager, player) 
		self.set_current_screen(main_screen)
		level = player.current_level
		level.initialize_screen(self, main_screen)

	def switch_to_pause_screen(self, player):
		controls = PauseControls(player)
		control_manager = ControlManager(controls)
		pause_screen = PauseScreen(control_manager, player)
		self.set_current_screen(pause_screen)