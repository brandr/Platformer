""" the screen that appears when the player opens its inventory.
"""

from gameimage import GameImage, DEFAULT_COLORKEY
from gamescreen import GameScreen
from dialog import WHITE, BLACK
from inventory import LANTERN, SWORD
from pygame import font, Surface

INVENTORY_PANE_WIDTH, INVENTORY_PANE_HEIGHT = 640, 480
INVENTORY_PANE_X, INVENTORY_PANE_Y = 80, 80
ITEM_GRID_WIDTH, ITEM_GRID_HEIGHT = INVENTORY_PANE_WIDTH - 64, INVENTORY_PANE_HEIGHT - 96
ITEM_GRID_X, ITEM_GRID_Y = 32, 48
ITEM_CELL_SIZE = 32
ITEM_ROWS, ITEM_COLS = 8, 6

class InventoryScreen(GameScreen):
	""" InventoryScreen( ControlManager, Player) -> InventoryScreen

	Shows the inventory screen. Allows some changes to be made, such as the current lantern mode.

	Attributes:

	player: The player whose inventory is being shown.
	"""
	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager) 
		self.player = player
		self.inventory_pane = self.draw_inventory_pane()
		
	def update(self):
		""" is.update( ) -> None

		Update the components of the inventory screen.
		"""
		self.draw_bg()
		self.screen_image.blit(self.inventory_pane, (INVENTORY_PANE_X, INVENTORY_PANE_Y))

	def draw_inventory_pane(self):
		""" is.draw_inventory_pane( ) -> Surface

		Generates an image representing the player's inventory.
		"""
		pane = Surface( (INVENTORY_PANE_WIDTH, INVENTORY_PANE_HEIGHT) )
		pane.fill(WHITE)
		text_font = font.Font("./fonts/FreeSansBold.ttf", 20)
		text_image = text_font.render("Inventory", 1, BLACK)
		pane.blit(text_image, ( 20, 20 ))
		self.draw_player_items(pane)
		return pane
		#TODO: fancier

	def draw_player_items(self, pane):
		""" is.draw_player_items( Surface ) -> None

		Draw the player's owned items onto the inventory pane.
		"""
		item_grid = self.item_grid()
		pane.blit(item_grid,( ITEM_GRID_X, ITEM_GRID_Y) )
		#TODO: blit the player's inventory contents onto the pane
		# make a grid of items (might not be necessary to draw lines) and blit the items as we grab their pictures.

	def item_grid(self):
		""" is.item_grid( ) -> Surface

		Generates a grid for showing the player's items.
		"""
		grid = Surface((ITEM_GRID_WIDTH, ITEM_GRID_HEIGHT))
		item_names = self.player.inventory.get_all_item_keys()
		index = 0
		for name in item_names:
			item_image = GameImage.load_image_file("./inventory_images/", name + ".bmp")
			item_image.set_colorkey(DEFAULT_COLORKEY)
			item_image.convert()
			x, y = index%ITEM_COLS, index/ITEM_COLS
			grid.blit(item_image, ( x*ITEM_CELL_SIZE, y*ITEM_CELL_SIZE))
			index += 1
		return grid