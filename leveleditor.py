import pygame
from pygame import *

class LevelEditor(object):
	#TODO: "dungeon" grid which shows all the rooms/levels in the dungeon
		#levels can be set to include different rooms
		#in the long run it may help to constrain the levels to only those
			#possible in the game
	#TODO: "level" grid which can be opened by expanding levels in the dungeon grid
	#TODO: make grid tiles an actual object type, possibly using inheritance (and maybe
		#making them abstract) so that the data they hold can be processed internally
		#but also displayed.

	TILE_SIZE = 32
	BLACK = Color("#000000")
	WHITE = Color("#FFFFFF")

	def __init__(self,dungeon_dimensions):
		self.dungeon_grid = self.dungeon_grid(dungeon_dimensions) 

		#this may eventually take in commands (such as clicking on tiles)
	def update(self,screen):
		TILE_SIZE = LevelEditor.TILE_SIZE
		screen.blit(self.dungeon_grid,(TILE_SIZE,TILE_SIZE)) #TEMPORARY
		pygame.display.update()

	def dungeon_grid(self,dimensions):
		#TODO: eventually make grid its own object type, and update the display with only grid_image (which is retrieved from the dungeon grid)
		dungeon_grid_image = LevelEditor.grid_menu("Dungeon",dimensions)
		return dungeon_grid_image

	@staticmethod
	def grid_menu(title,dimensions): #could make grid menu its own class, and menu image merely a data member
		TILE_SIZE = LevelEditor.TILE_SIZE
		width = dimensions[0]
		height = dimensions[1]
		grid_image = LevelEditor.empty_grid(width,height)
		menu_image = Surface((TILE_SIZE*(width+2),TILE_SIZE*(height+3)))
		menu_image.fill(LevelEditor.WHITE)
		menu_image.blit(grid_image,(TILE_SIZE,TILE_SIZE*2))
		# Display some text
		font = pygame.font.Font(None, 36)
		text = font.render(title, 1, (10, 10, 10))
		textpos = text.get_rect()
		textpos.left,textpos.top = TILE_SIZE,TILE_SIZE/2 #temp
		menu_image.blit(text, textpos)
		return menu_image

	@staticmethod
	def empty_grid(width,height):
		TILE_SIZE = LevelEditor.TILE_SIZE
		if(width <= 0 or height <= 0):
			return None
		grid = Surface((width*TILE_SIZE,height*TILE_SIZE))
		grid.fill(LevelEditor.BLACK)
		for y in range (0,height):
			for x in range(0,width):
				blank_tile = Surface((TILE_SIZE,TILE_SIZE))
				blank_tile.fill(LevelEditor.WHITE)
				grid_blank_tile = LevelEditor.grid_tile(blank_tile)
				tile_x = TILE_SIZE*x+1
				tile_y = TILE_SIZE*y+1
				grid.blit(grid_blank_tile,(tile_x,tile_y))
		
		#TODO
		return grid

		#a tile which will fit within grid lines
	@staticmethod	
	def grid_tile(full_tile):
		grid_tile = Surface((full_tile.get_width()-2,full_tile.get_height()-2))
		grid_tile.blit(full_tile, (1, 1), (1, 1, grid_tile.get_width(), grid_tile.get_height()))
		return grid_tile