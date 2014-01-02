import pygame
from pygame import *
import grid
from grid import *
import scrollpane
from scrollpane import *
import table
from table import *
import levelselectcell
from levelselectcell import *

TILE_SIZE = 32

class LevelEditor(object):
	#TODO: make it so rectangles (and only rectangles) can be selected from the dungeon grid, and these can be used to define levels.

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
		#these would be very different from actual levels (might be called LevelDta)

	def __init__(self,dungeon_dimensions):
		dungeon_grid = self.dungeon_grid(dungeon_dimensions)
		dungeon_grid_menu = LevelEditor.grid_menu("Dungeon Map",dungeon_grid,TILE_SIZE,TILE_SIZE)
		level_select_x = dungeon_grid_menu.x+dungeon_grid_menu.width+TILE_SIZE
		level_select_y = dungeon_grid_menu.y
		level_select_menu = LevelEditor.level_select_menu(level_select_x,level_select_y)
		self.current_level = None #this represents the level currently selected for editing.
		self.components = [dungeon_grid_menu,level_select_menu]

		#this may eventually take in commands (such as clicking on tiles)
	def update(self,screen):
		for c in self.components: #could change this to m in self.menus, or some very general object like "guiComponent"
			c.update()
			screen.blit(c.image,(c.x,c.y))
		pygame.display.update()

	def button_at(self,pos):
		for c in self.components:
			if c.contains(pos):
				relative_pos = c.relative_pos(pos)
				return c.button_at(relative_pos)
		return None

	def dungeon_grid(self,dimensions):
		x,y = TILE_SIZE,TILE_SIZE*2 #TEMP
		return Grid(x,y,dimensions[0],dimensions[1],TILE_SIZE)

	@staticmethod
	def level_select_menu(x,y): #do I need more args?
		menu = GuiComponent(x,y,TILE_SIZE*12,TILE_SIZE*10)
		menu.addText("Level List",32,TILE_SIZE, TILE_SIZE/2)
		level_select_list = LevelEditor.level_select_list(TILE_SIZE,TILE_SIZE,(TILE_SIZE*10,TILE_SIZE))
		pane_dimensions = (TILE_SIZE*12,TILE_SIZE*6)
		pane_window_dimensions = (pane_dimensions[0]-TILE_SIZE*2,pane_dimensions[1]-TILE_SIZE*1.75)
		level_select_pane = ScrollPane(  0,        TILE_SIZE*1.5,pane_dimensions,pane_window_dimensions,level_select_list)
		add_level_button = LevelEditor.add_level_button(TILE_SIZE,TILE_SIZE*8,level_select_list)
		menu.insert(level_select_pane)
		menu.insert(add_level_button)
		return menu

	@staticmethod #might need to make a level select list class which inherits from Table
	def level_select_list(x,y,dimensions):
		cell_list = []
		cell_list.append([])
		cell_list[0].append(LevelSelectCell(0,0,dimensions[0],dimensions[1]))
		level_list = Table(x,y,1,1,(dimensions[0],dimensions[1]),cell_list)
		#TODO: make level select list a resizable list of levels, one of which can be selected at a time.
			#  the user can also add or remove levels from the list, and possibly name them.
		return level_list

	@staticmethod
	def add_level_button(x,y,level_select_list):
		add_level_image = Surface((TILE_SIZE*4,TILE_SIZE))
		add_level_image.fill(Color("#AAAA00"))
		add_level_button = Button(add_level_image,x,y,level_select_list.insertRow,(None))
		add_level_button.addText("Add Level",22,TILE_SIZE/8,TILE_SIZE/8)
		return add_level_button

	#TODO: each added level cell needs to contain some sort of guicomponent that shows the levelName, along with buttons
		#  for "edit level", "resize level", and probably others.

	@staticmethod
	def grid_menu(title,grid,x,y): #could make grid menu its own class, and menu image merely a data member
		width,height = TILE_SIZE*(grid.width()+2),TILE_SIZE*(grid.height()+3)
		menu = GuiComponent(x,y,width,height)
		menu.addText(title,32,TILE_SIZE,TILE_SIZE/2)
		menu.insert(grid)
		return menu