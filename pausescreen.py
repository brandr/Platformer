""" the screen that appears when the player pauses the game.
"""

from gamescreen import GameScreen
from mappane import MapPane
from dialog import WHITE, BLACK
import pygame
from pygame import Surface, font 

PAUSE_PANE_WIDTH, PAUSE_PANE_HEIGHT = 400, 300
PAUSE_PANE_X, PAUSE_PANE_Y = 200, 170
RESUME, OPTIONS, QUIT = "Resume", "Options", "Quit"
PAUSE_OPTIONS = [RESUME, OPTIONS, QUIT]

class PauseScreen(GameScreen):
	""" PauseScreen( ControlManager, Player) -> PauseScreen

	Currently, the pause screen only shows the map pane. If there are multiple screens then this class
	will need to be restructured.

	Attributes:

	player: The player whose location is shown on the map pane.

	level_image: A Surface representing the level the player was on the moment it was paused.

	pause_pane: A rectangular pane showing pause options.
	"""
	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager) 
		self.player = player
		self.level_image = self.player.current_level.screen
		self.pause_option_index = 0

	def update(self):
		""" ps.update( ) -> None

		Redraw the pause screen's components.
		"""
		self.draw_bg()
		self.screen_image.blit(self.level_image, (0, 0))
		self.screen_image.blit(self.draw_pause_pane(), (PAUSE_PANE_X, PAUSE_PANE_Y))

	def select(self):
		""" pc.select( ) -> None

		Select the current pause option.
		"""
		pause_method = PAUSE_OPTION_METHODS[self.pause_option_index]
		pause_method(self)

	def unpause(self):
		""" pc.unpause( ) -> None

		Resume the game.
		"""
		self.player.unpause_game()

	def open_options(self):
		""" pc.open_options( ) -> None

		Open up options such as changing controls.
		"""
		#TODO: probably handle this by opening up a new control context, or leaving the screen the same but making some display flag for options vs normal pause display
		pass 

	def quit_game(self):
		""" pc.quit_game( ) -> None

		Quit the game.
		"""
		print "Game was ended by user."
		raise(SystemExit)

	def draw_pause_pane(self):
		""" ps.draw_pause_pane( ) -> Surface

		Draw an image representing the pause pane.
		"""
		pane = Surface((PAUSE_PANE_WIDTH, PAUSE_PANE_HEIGHT))
		pane.fill(WHITE)
		text_font = font.Font("./fonts/FreeSansBold.ttf", 28)
		text_image = text_font.render("GAME PAUSED", 1, BLACK)
		pane.blit(text_image, ( 100, 20 ))
		pane.blit(self.draw_pause_options_pane(), (8, 64))
		return pane

	def draw_pause_options_pane(self):
		""" ps.draw_pause_options_pane( ) -> Surface

		Draw an image representing the pane that shows the options available while paused.
		"""
		pane = Surface((PAUSE_PANE_WIDTH - 16, PAUSE_PANE_HEIGHT - 40))
		pane.fill(WHITE)
		points = [(0, 0), ( PAUSE_PANE_WIDTH - 18, 0 ), ( PAUSE_PANE_WIDTH - 18, PAUSE_PANE_HEIGHT - 74 ), ( 0, PAUSE_PANE_HEIGHT - 74 ) ]
		pygame.draw.lines(pane, BLACK, True, points, 2)
		
		text_font = font.Font("./fonts/FreeSansBold.ttf", 28)
		for i in xrange(len(PAUSE_OPTIONS)):
			text_image = text_font.render(PAUSE_OPTIONS[i], 1, BLACK)
			pane.blit(text_image, ( 40, 8 + i*40))
		select_cursor = Surface((16, 16)) #might want to replace this with a better-looking cursor
		pane.blit( select_cursor, ( 12, 16 + self.pause_option_index*40))
		return pane

	def move_cursor(self, direction):
		""" ps.move_cursor( int ) -> None

		Move the cursor to select a different pause option.
		"""
		self.pause_option_index = (self.pause_option_index + direction)%3

PAUSE_OPTION_METHODS = [
	PauseScreen.unpause,
	PauseScreen.open_options,
	PauseScreen.quit_game
]