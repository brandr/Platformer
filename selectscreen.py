""" An abstract screen type specifically used for selecting from 2D lists of text options.
"""

from gamescreen import GameScreen
from dialog import WHITE, BLACK
import pygame
from pygame import Surface, Color, font

SELECTION_BAR_COLOR = Color("#00FFFF")

class SelectScreen(GameScreen):
	""" SelectScreen( ControlManager, Player) -> SelectScreen

	A select screen is essentially an abstract container for a set of text options, one of which
	may be selected at a time. A selection can be confirmed by pressing enter, prompting some action.

	Attributes:

	player: The player whose location is shown on the map pane.

	bg_image: A Surface representing the background that this SelectScreen's components should be blitted over.

	option_index: The index of the currently selected option.

	screen_key: A text key used to access information for building a specific select pane.

	select_options: A set of ordered methods associated with different options available on this select screen.
	"""
	def __init__(self, control_manager, player, bg_image, screen_key, select_options, select_option_methods):
		GameScreen.__init__(self, control_manager) 
		self.player = player
		self.bg_image = bg_image
		self.screen_key = screen_key
		self.select_options = select_options
		self.select_option_methods = select_option_methods
		self.option_index = 0
		self.option_font_size = 28
		dimensions = self.get_dimensions()
		self.select_bar = Surface((dimensions[0] - 18, self.option_font_size + 6))
		self.select_bar.fill(SELECTION_BAR_COLOR)

	def update(self):
		""" ss.update( ) -> None

		Redraw the select screen's components.
		"""
		self.draw_bg()
		self.screen_image.blit(self.bg_image, (0, 0))
		pane_coords = SCREEN_DATA_MAP[self.screen_key][COORDS]
		self.screen_image.blit(self.draw_select_pane(), ( pane_coords[0], pane_coords[1]) )

	def select(self):

		""" ss.select( ) -> None

		Select the current option, executing its associated action.
		"""
		select_method = self.select_option_methods[self.option_index]
		select_method(self)

	def draw_select_pane(self):
		""" ss.draw_select_pane( ) -> Surface

		Draw an image representing the select pane.
		"""
		pane_dimensions = SCREEN_DATA_MAP[self.screen_key][DIMENSIONS]
		pane = Surface( ( pane_dimensions[0], pane_dimensions[1] ) )
		pane.fill(WHITE)
		return pane

	def draw_select_options_pane(self):
		""" ss.draw_select_options_pane( Surface ) -> Surface

		Draw an image representing the pane that shows the options available.
		"""
		full_dimensions = SCREEN_DATA_MAP[self.screen_key][DIMENSIONS]
		dimensions = SCREEN_DATA_MAP[self.screen_key][OPTIONS_DIMENSIONS]
		offset = SCREEN_DATA_MAP[self.screen_key][OPTIONS_COORDS]
		end_x, end_y = min( offset[0] + dimensions[0], full_dimensions[0] ), min( offset[1] + dimensions[1], full_dimensions[1] ) - offset[1]
		pane = Surface( ( end_x, end_y ) )
		pane.fill(WHITE)
		points = [(0, 0), ( end_x - 2, 0 ), ( end_x - 2, end_y - 8 ), ( 0, end_y - 8 ) ]
		pygame.draw.lines(pane, BLACK, True, points, 2)
		text_font = font.Font("./fonts/FreeSansBold.ttf", self.option_font_size)	
		space = self.option_font_size + 8
		pane.blit(self.select_bar, ( 2,  self.option_index*space + 2))
		for i in xrange(len(self.select_options)):
			text_image = text_font.render(self.select_options[i], 1, BLACK)
			pane.blit(text_image, ( space, 8 + i*space))
		#select_cursor = Surface((14, 14)) 							# might want to replace this with a better-looking cursor
		#pane.blit( select_cursor, ( 6, 14 + self.option_index*space))
		return pane

	def move_cursor(self, direction):
		""" ss.move_cursor( int ) -> None

		Move the cursor to select a different option.
		"""
		self.option_index = (self.option_index + direction)%len(self.select_options)

	def get_dimensions(self):
		""" ss.get_dimensions( ) -> (int, int)

		Get the dimensions in pixels of this selectscreen.
		"""
		return SCREEN_DATA_MAP[self.screen_key][DIMENSIONS]

# select screen types
PAUSE, OPTIONS, CONTROLS = "pause", "options", "controls"

# select screen attributes
COORDS = "coords"
DIMENSIONS = "dimensions"
OPTIONS_COORDS = "options_coords"
OPTIONS_DIMENSIONS = "options_dimensions"

SCREEN_DATA_MAP = {
	PAUSE: {
		COORDS: ( 200, 170 ),
		DIMENSIONS: ( 400, 300 ),
		OPTIONS_COORDS : ( 8, 64 ),
		OPTIONS_DIMENSIONS: ( 384, 260 )
	},
	OPTIONS: {
		COORDS: ( 180, 70 ),
		DIMENSIONS: ( 440, 500 ),
		OPTIONS_COORDS : ( 8, 64 ),
		OPTIONS_DIMENSIONS: ( 414, 460 )
	}
	,
	CONTROLS: {
		COORDS: ( 180, 70 ),
		DIMENSIONS: ( 440, 500 ),
		OPTIONS_COORDS : ( 8, 64 ),
		OPTIONS_DIMENSIONS: ( 414, 460 )
	}
}