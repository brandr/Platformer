""" A pane showing a map of the the dungeon that the player is in.
"""

from pygame import Color, Surface, draw
from pygame.draw import *

WHITE = Color("#FFFFFF")
RED = Color("#FF0000")
GREEN = Color("#00FF00")
PURPLE = Color("#FF00FF")
CYAN = Color("#00FFFF")

MAP_PANE_WIDTH, MAP_PANE_HEIGHT = 400, 400
ROOM_TILE_WIDTH, ROOM_TILE_HEIGHT = MAP_PANE_WIDTH/20, MAP_PANE_HEIGHT/20

class MapPane: #inheritance?
	""" TODO: docstring"""
	def __init__(self, player, x, y):
		self.player, self.x, self.y = player, x, y
		self.pane_image = Surface((MAP_PANE_WIDTH, MAP_PANE_HEIGHT)) #TEMP
		self.blink_index = 0
		self.draw_borders()
		
	def update(self):
		self.advance_blink_index()
		self.draw_map()

	def draw_borders(self):
		corners = [(0, 0), (MAP_PANE_WIDTH - 2, 0), (MAP_PANE_WIDTH - 2, MAP_PANE_HEIGHT - 2), (0, MAP_PANE_HEIGHT - 2)] #TEMP
		lines(self.pane_image, WHITE, True, corners, 2)

	def draw_map(self):	 
		current_level = self.player.current_level
		dungeon = current_level.dungeon

		current_room_image = MapPane.draw_current_room_image()
		unexplored_room_image = MapPane.draw_unexplored_room_image()
		for L in dungeon.dungeon_levels:
			if not L.is_explored(): continue
			origin = L.origin
			width, height = L.room_width(), L.room_height()
			pixel_coords = ((origin[0] + 1)*ROOM_TILE_WIDTH, (origin[1] + 1)*ROOM_TILE_HEIGHT)
			explored_level_image = MapPane.draw_explored_level_image(width, height, L.outdoors)
			self.pane_image.blit(explored_level_image, pixel_coords)
			for y in xrange(height):
				for x in xrange(width):
					if not L.explored_at(x, y):
						pixel_coords = ((origin[0] + x + 1)*ROOM_TILE_WIDTH, (origin[1] + y + 1)*ROOM_TILE_HEIGHT)
						self.pane_image.blit(unexplored_room_image, pixel_coords)
		current_global_coords = current_level.global_coords(self.player.coordinates())
		current_pixel_coords = ( (current_global_coords[0] + 1)*ROOM_TILE_WIDTH, (current_global_coords[1] + 1 )*ROOM_TILE_HEIGHT)
		if self.blink_index > 20:
			self.pane_image.blit(current_room_image, current_pixel_coords)
			if self.blink_index > 40:
				self.blink_index = 0

	def advance_blink_index(self):
		self.blink_index += 1
					
	@staticmethod
	def draw_explored_level_image(width, height, sunlit):
		color = None
		if sunlit: color = GREEN
		else: color = PURPLE
		explored_level_image = Surface((width*ROOM_TILE_WIDTH, height*ROOM_TILE_HEIGHT))
		explored_level_image.fill(color)
		corners = [(0, 0), (width*ROOM_TILE_WIDTH - 2, 0), (width*ROOM_TILE_WIDTH - 2, height*ROOM_TILE_HEIGHT - 2), (0, height*ROOM_TILE_HEIGHT - 2)] #TEMP
		lines(explored_level_image, WHITE, True, corners, 2)
		return explored_level_image

	@staticmethod
	def draw_unexplored_room_image():
		return Surface((ROOM_TILE_WIDTH, ROOM_TILE_HEIGHT))

	@staticmethod
	def draw_current_room_image():	
		current_room_image = Surface((ROOM_TILE_WIDTH, ROOM_TILE_HEIGHT))
		current_room_image.fill(CYAN)
		return current_room_image

