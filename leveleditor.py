import pygame
from pygame import *
import grid
from grid import *

class LevelEditor(object):
	#TODO: "dungeon" grid which shows all the rooms/levels in the dungeon
		#levels can be set to include different rooms
		#in the long run it may help to constrain the levels to only those
			#possible in the game
		#somehow indicate which dungeon grid tiles have levels in them/which are empty,
			#and possibly some information about the corresponding levels.
	#TODO: "level" grid which can be opened by expanding levels in the dungeon grid
	#TODO: make grid tiles an actual object type, possibly using inheritance (and maybe
		#making them abstract) so that the data they hold can be processed internally
		#but also displayed.
	#IDEA: upon clicking on a tile in the dungeon grid, the user prompts the level grid to change to the
		#level corresponding to that tile, and for all that level's tiles to be highlighted somehow in the dungeon grid.
	#might need a special object type corresponding to levels for the editor to work with.
		#these would be very different from actual levels

	TILE_SIZE = 32
	BLACK = Button.BLACK #Color("#000000")
	WHITE = Button.WHITE #Color("#FFFFFF")

	def __init__(self,dungeon_dimensions):
		self.dungeon_grid = self.dungeon_grid(dungeon_dimensions)
		self.current_level = None #this represents the level currently selected for editing.
		self.grids = [self.dungeon_grid]
		#self.buttons = [self.dungeon_grid]	#IDEA: "buttons" array represents all interactable objects. could do the same for grids.

		#this may eventually take in commands (such as clicking on tiles)
	def update(self,screen):
		TILE_SIZE = LevelEditor.TILE_SIZE
		for g in self.grids: #could change this to m in self.menus, or some very general object like "guiComponent"
			g.update()
			screen.blit(g.image,(g.x,g.y))
			#TODO: blit the image from each grid (or menu?) against the screen
		#screen.blit(self.dungeon_grid,(TILE_SIZE,TILE_SIZE)) #TEMPORARY
		pygame.display.update()

	def dungeon_grid(self,dimensions):
		#TODO: consider making the grid menu its own object type, which contains the grid
		TILE_SIZE = LevelEditor.TILE_SIZE
		x,y = TILE_SIZE,TILE_SIZE #TEMP
		return Grid(x,y,dimensions[0],dimensions[1],LevelEditor.TILE_SIZE)
		#dungeon_grid_image = LevelEditor.grid_menu("Dungeon",dimensions)
		#return dungeon_grid_image

	@staticmethod
	def grid_menu(title,dimensions): #could make grid menu its own class, and menu image merely a data member
		def title_text(text,offset):	#TODO: consider other args, and maybe make this its own method outside this one (more general than "title")
			font = pygame.font.Font(None, 36)
			text = font.render(text, 1, (10, 10, 10)) #not sure what these args mean
			textpos = text.get_rect()
			textpos.left,textpos.top = (offset[0],offset[1])#temp
			return text,textpos
		TILE_SIZE = LevelEditor.TILE_SIZE
		width = dimensions[0]
		height = dimensions[1]
		grid_image = LevelEditor.empty_grid(width,height)
		menu_image = Surface((TILE_SIZE*(width+2),TILE_SIZE*(height+3)))
		menu_image.fill(LevelEditor.WHITE)
		menu_image.blit(grid_image,(TILE_SIZE,TILE_SIZE*2))
		# Display some text
		text,textpos = title_text(title,(TILE_SIZE,TILE_SIZE/2)) 
		menu_image.blit(text, textpos)
		return menu_image

	@staticmethod
	def empty_grid(width,height):
		#TODO: make an actual grid object (from grid.py) here
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
		#(in the process of moving this to Grid class)
	@staticmethod	
	def grid_tile(full_tile):
		grid_tile = Surface((full_tile.get_width()-2,full_tile.get_height()-2))
		grid_tile.blit(full_tile, (1, 1), (1, 1, grid_tile.get_width(), grid_tile.get_height()))
		return grid_tile