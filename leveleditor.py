import pygame
from pygame import *
import grid
from grid import *

TILE_SIZE = 32

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

	
	#BLACK = Button.BLACK #Color("#000000")
	#WHITE = Button.WHITE #Color("#FFFFFF")

	def __init__(self,dungeon_dimensions):
		TILE_SIZE 
		dungeon_grid = self.dungeon_grid(dungeon_dimensions)
		dungeon_grid_menu = LevelEditor.grid_menu("Dungeon",dungeon_grid,TILE_SIZE,TILE_SIZE)
		self.current_level = None #this represents the level currently selected for editing.
		self.components = [dungeon_grid_menu]
		#self.buttons = [self.dungeon_grid]	#IDEA: "buttons" array represents all interactable objects. could do the same for grids.

		#this may eventually take in commands (such as clicking on tiles)
	def update(self,screen):
		#TILE_SIZE = LevelEditor.TILE_SIZE
		for c in self.components: #could change this to m in self.menus, or some very general object like "guiComponent"
			c.update()
			screen.blit(c.image,(c.x,c.y))
			#TODO: blit the image from each grid (or menu?) against the screen
		pygame.display.update()

	def button_at(self,pos):
		for c in self.components:
			if c.contains(pos):
				relative_pos = c.relative_pos(pos)
				return c.button_at(relative_pos)
			#print pos
		return None

	def dungeon_grid(self,dimensions):
		#TODO: consider making the grid menu its own object type, which contains the grid
		#TILE_SIZE = LevelEditor.TILE_SIZE
		x,y = TILE_SIZE,TILE_SIZE*2 #TEMP
		return Grid(x,y,dimensions[0],dimensions[1],TILE_SIZE)
		#dungeon_grid_image = LevelEditor.grid_menu("Dungeon",dimensions)
		#return dungeon_grid_image

	@staticmethod
	def grid_menu(title,grid,x,y): #could make grid menu its own class, and menu image merely a data member
		def title_text(text,offset):	#TODO: consider other args, and maybe make this its own method outside this one (more general than "title")
			font = pygame.font.Font(None, 36)
			text = font.render(text, 1, (10, 10, 10)) #not sure what these args mean
			textpos = text.get_rect()
			textpos.left,textpos.top = (offset[0],offset[1])#temp
			return text,textpos
		#TILE_SIZE = LevelEditor.TILE_SIZE
		width,height = TILE_SIZE*(grid.width()+2),TILE_SIZE*(grid.height()+3)
		menu = GuiComponent(x,y,width,height)
		text,textpos = title_text(title,(TILE_SIZE,TILE_SIZE/2)) 
		text_component = GuiComponent(textpos.left,textpos.top,textpos.width,textpos.height,WHITE,text)
		menu.insert(grid)
		menu.insert(text_component)
		return menu

	@staticmethod
	def empty_grid(width,height):
		#TODO: make an actual grid object (from grid.py) here
		#TILE_SIZE = LevelEditor.TILE_SIZE
		if(width <= 0 or height <= 0):
			return None
		grid = Surface((width*TILE_SIZE,height*TILE_SIZE))
		grid.fill(BLACK)
		for y in range (0,height):
			for x in range(0,width):
				blank_tile = Surface((TILE_SIZE,TILE_SIZE))
				blank_tile.fill(WHITE)
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