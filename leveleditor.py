import pygame
from pygame import *

class LevelEditor(object):

	TILE_SIZE = 32

	def __init__(self):
		pass

	def update(self,screen):
		TILE_SIZE = LevelEditor.TILE_SIZE
		screen.blit(self.empty_grid(4,4),(TILE_SIZE,TILE_SIZE)) #TEMP
		pygame.display.update()

	def empty_grid(self,width,height):
		TILE_SIZE = LevelEditor.TILE_SIZE
		if(width <= 0 or height <= 0):
			return None
		grid = Surface((width*TILE_SIZE,height*TILE_SIZE))
		grid.fill(Color("#000000"))
		for y in range (0,height):
			for x in range(0,width):
				blank_tile = Surface((TILE_SIZE,TILE_SIZE))
				blank_tile.fill(Color("#FFFFFF"))
				grid_blank_tile = self.grid_tile(blank_tile)
				tile_x = TILE_SIZE*x+1
				tile_y = TILE_SIZE*y+1
				grid.blit(grid_blank_tile,(tile_x,tile_y))
		
		#TODO
		return grid

	def grid_tile(self,full_tile):
		grid_tile = Surface((full_tile.get_width()-2,full_tile.get_height()-2))
		grid_tile.blit(full_tile, (1, 1), (1, 1, grid_tile.get_width(), grid_tile.get_height()))
		return grid_tile