import levelselectcell
from levelselectcell import *
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

MAX_LEVELS = 99


#TODO:consider separating out the levelselectwindow into its own class....
class LevelSelectContainer(Box):
	def __init__(self,position,dimensions):
		Box.__init__(self,dimensions[0],dimensions[1])
		self.topleft = (position[0],position[1])

		self.level_count = 0
		self.selected_level_cell = None #TODO: make it possible to select a level cell (and make it visually clear which one is selected)

		level_select_label = Label("Dungeon Levels:")

		self.level_data_table = Table(MAX_LEVELS,1)
		self.level_window = self.level_window(dimensions[0]-36,dimensions[1]-128,self.level_data_table)
		self.selected_level_label = self.selected_level_label(self.level_window.left,self.level_window.bottom+12)

		self.add_level_button = self.add_level_button(224,6)
		self.rename_level_button = self.rename_level_button(self.selected_level_label.left,self.selected_level_label.bottom+8)
		self.level_name_entry = self.rename_level_entry_field(self.rename_level_button.right+8, self.rename_level_button.top)

		self.add_child(level_select_label)
		self.add_child(self.level_window)
		self.add_child(self.selected_level_label)

		self.add_child(self.add_level_button)
		self.add_child(self.rename_level_button)
		self.add_child(self.level_name_entry)

		#TODO: edit level button (will require processing Dungeon/Room Data, also Dungeon grid)
		#TODO: resize level button
		#TODO: delete level button(NICK)
		#TODO: buttons for any levelData attributes external to rooms

		self.updateSelectedLevel()

	#buttons/entry fields

	def add_level_button(self,x,y):
		button = Button("Add a level")
		button.topleft = (x,y)
		button.connect_signal (SIG_CLICKED, self.addLevel)
		return button

	def rename_level_button(self,x,y):
		button = Button("Rename")
		button.topleft = x,y
		button.connect_signal(SIG_CLICKED,self.renameSelectedLevel)
		return button

	def rename_level_entry_field(self,x,y):
		entry = Entry(self.selected_level_string())
		entry.topleft = x,y
		return entry

	#level window

	def level_window(self,width,height,level_data_table):
		window = ScrolledWindow(width,height)
		window.set_child(level_data_table)
		window.connect_signal(SIG_MOUSEDOWN,self.clickLevelCell) #TODO: make the table "select" a level
		window.topleft = (18,45)
		return window

	def selected_level_label(self,x,y):
		#label_text = "Selected Level: " + self.selected_level_string()
		label = Label("Selected Level:              ")
		label.topleft = x,y
		return label

	def selected_level_string(self):
		if(self.selected_level_cell == None): return "None"
		return self.selected_level_cell.get_name()

		#methods to alter the level data
	
	def addLevel(self):
		level_name = "level "+str(self.level_count)
		added_level_cell = LevelSelectCell(level_name)
		self.level_data_table.add_child(self.level_count,0,added_level_cell)
		self.level_count += 1

	def renameSelectedLevel(self):
		if(self.selected_level_cell == None): return
		new_level_name = self.level_name_entry.text
		self.selected_level_cell.rename_level(new_level_name)
		self.updateSelectedLevel()

	def clickLevelCell(self,event):
		coords = event.pos
		screen_offset = (self.left + self.level_window.left,self.top + self.level_window.top)
		relative_coords = (coords[0]-screen_offset[0],coords[1]-screen_offset[1])
		if relative_coords[0] > self.level_window.vscrollbar.left or relative_coords[1] > self.level_window.hscrollbar.top: return
		y_scroll_offset = self.level_window.vscrollbar.value
		#adjusted coords represent the coordinates of the clicked cell, in pixels, 
		#assuming that 0,0 is the upper left of the top cell (regardless of scrolling).
		adjusted_coords = (relative_coords[0],relative_coords[1]+y_scroll_offset) 
		selected_level_cell = self.cell_at(adjusted_coords)
		self.selectLevelCell(selected_level_cell) #this might go in LevelSelectTable if tthat ends up being a different class.

	def selectLevelCell(self,level_cell):
		if level_cell == None or self.selected_level_cell == level_cell:
			self.updateSelectedLevel()
			return #might also want to deselect current level cell
		if(self.selected_level_cell != None):
			self.selected_level_cell.deselect()
		level_cell.select()
		self.selected_level_cell = level_cell
		self.updateSelectedLevel()

	def updateSelectedLevel(self):
		self.selected_level_label.set_text("Selected Level: "+self.selected_level_string())
		self.level_name_entry.set_text(self.selected_level_string())
		if self.selected_level_cell == None: 
			self.rename_level_button.set_state(Constants.STATE_INSENSITIVE)
			self.rename_level_button.sensitive = False
			self.level_name_entry.set_state(Constants.STATE_INSENSITIVE)
			self.level_name_entry.sensitive = False
		else: 
			self.rename_level_button.set_state(Constants.STATE_NORMAL)
			self.rename_level_button.sensitive = True
			self.level_name_entry.set_state(Constants.STATE_NORMAL)
			self.level_name_entry.sensitive = True

	def cell_at(self,coords):
		height = CELL_HEIGHT+2
		row = int(coords[1]/height)
		col = 0	#since the level data cells have only one column, we always use the first index.
		#print "CELL INDEX: "+str((row,col))	#keep prints around for testing until the cell finding process is finalized.
		if (row, col) not in self.level_data_table.grid:
		#	print "Nahhh."
		#	print ""
			return
		cell = self.level_data_table.grid[(row,col)]
		return cell
		#print "At "+ str((row,col))+": "+str(cell)
		#print ""

	@staticmethod
	def empty_level_table():
		table = Table (1, 1)
		table.spacing = 5
		table.topleft = 5, 5
		return table