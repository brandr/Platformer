""" the screen that appears when the player pauses the game.
"""

from selectscreen import SelectScreen, PAUSE, SCREEN_DATA_MAP, OPTIONS_COORDS
from dialog import WHITE, BLACK
import pygame
from pygame import Surface, font 

class PauseScreen(SelectScreen):
	""" PauseScreen( ControlManager, Player) -> PauseScreen

	The pause screen allows the player to resume, change options, or quit the game.
	It does this through the abstract interface of the SelectScreen.

	Attributes:

	level_image: A Surface representing the level the player was on the moment it was paused.
	"""

	def __init__(self, control_manager, player):
		level_image = player.current_level.screen
		SelectScreen.__init__(self, control_manager, player, level_image, PAUSE, PAUSE_OPTIONS, PAUSE_OPTION_METHODS ) 

	def unpause(self):
		""" ps.unpause( ) -> None

		Resume the game.
		"""
		self.player.unpause_game()

	def open_options(self):
		""" ps.open_options( ) -> None

		Open up options such as changing controls.
		"""
		self.player.current_level.screen_manager.switch_to_options_screen(self.player)

	def quit_game(self):
		""" ps.quit_game( ) -> None

		Quit the game.
		"""
		print "Game was ended by user."
		raise(SystemExit)

	def draw_select_pane(self):
		""" ps.draw_select_pane( ) -> Surface

		Draw an image representing the pause pane.
		"""
		pane = SelectScreen.draw_select_pane(self)
		text_font = font.Font("./fonts/FreeSansBold.ttf", 28)
		text_image = text_font.render("GAME PAUSED", 1, BLACK)
		pane.blit(text_image, ( 100, 20 ))
		coords = SCREEN_DATA_MAP[PAUSE][OPTIONS_COORDS]
		pane.blit(self.draw_select_options_pane(), (coords[0], coords[1]))	# TODO: fetch the 8, 64 from a the map in selectscreen.py
		return pane

RESUME, OPTIONS, QUIT = "Resume", "Options", "Quit"
PAUSE_OPTIONS = [RESUME, OPTIONS, QUIT]

PAUSE_OPTION_METHODS = [
	PauseScreen.unpause,
	PauseScreen.open_options,
	PauseScreen.quit_game
]