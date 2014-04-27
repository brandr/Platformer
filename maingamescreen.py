""" the main screen for playing the game. Most of the player's actions take place here.
"""

from gamescreen import *

class MainGameScreen(GameScreen):

	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager)
		self.width, self.height = WIN_WIDTH, WIN_HEIGHT
		self.player = player
		#self.layers = [3] # background (tile) layer, entity layer, dialogue layer

	def update(self):
		self.level_update()
		self.effects_update()

	def level_update(self):
		self.player.current_level.update(False, False, False, False, False, False)
		#coords = self.player.coordinates()
		#center_x, center_y = coords[0], coords[1]
		#half_width, half_height = MAP_PANE_WIDTH/(2 * TILE_WIDTH), MAP_PANE_HEIGHT/(2 * TILE_HEIGHT)
		#x1, y1 = center_x - half_width, center_y - half_height
		#x2, y2 = center_x + half_width, center_y + half_height
		#level_map = self.player.current_level.level_map_section(x1, y1, x2, y2)
		#Pane.update(self, level_map)

	def effects_update(self):
		pass #

		#TODO: move clear and draw_pane_image up in inheritance after translating them to platformer.
	def clear(self):
		self.contents = Surface((self.width, self.height))

	def draw_pane_image(self):
		self.pane_image.blit(self.contents, (2, 2))
		return self.pane_image