import dungeongrid
from dungeongrid import *

MAX_DUNGEON_ROWS = 16
MAX_DUNGEON_COLS = 16
LEFT_MOUSE_BUTTON = 1

class DungeonGridContainer(Box):
	def __init__(self,level_select_container,position,dimensions): #TODO: make level_select_container do something
		Box.__init__(self,dimensions[0],dimensions[1])
		self.topleft = (position[0],position[1])
		self.level_select_container = level_select_container
		level_select_container.dungeon_grid_container = self

		dungeon_grid_label = Label("Dungeon Grid:")

		self.dungeon_grid = DungeonGrid(level_select_container,MAX_DUNGEON_ROWS,MAX_DUNGEON_COLS)
		self.dungeon_window = self.dungeon_window(dimensions[0]-36,dimensions[1]-128,self.dungeon_grid)#TODO

		self.add_child(dungeon_grid_label)
		self.add_child(self.dungeon_window)

	def dungeon_window(self,width,height,dungeon_grid):
		window = ScrolledWindow(width,height)
		window.set_child(dungeon_grid)
		window.topleft = (18,45)
		window.connect_signal(SIG_MOUSEDOWN,self.clickDungeonCell)#self.dungeon_grid.clickDungeonCell,offset) #TODO: make it possible to select grid parts
		#window.set_state(Constants.STATE_INSENSITIVE)
		return window

	def clickDungeonCell(self,event):
		#TODO: consider only allowing level resizing after pressing the resize level button
		if(event.button != LEFT_MOUSE_BUTTON or self.level_select_container.selected_level_cell == None): return #IDEA: consider allowing the use of differnt buttons for different actions
		coords = event.pos
		screen_offset = (self.left + self.dungeon_window.left,self.top + self.dungeon_window.top)
		relative_coords = (coords[0]-screen_offset[0],coords[1]-screen_offset[1])
		if relative_coords[0] > self.dungeon_window.vscrollbar.left or relative_coords[1] > self.dungeon_window.hscrollbar.top: return
		x_scroll_offset = self.dungeon_window.hscrollbar.value
		y_scroll_offset = self.dungeon_window.vscrollbar.value
		adjusted_coords = (relative_coords[0]+x_scroll_offset,relative_coords[1]+y_scroll_offset) 
		selected_dungeon_cell = self.dungeon_grid.cell_at(adjusted_coords)
		self.dungeon_grid.leftClickDungeonCell(selected_dungeon_cell)