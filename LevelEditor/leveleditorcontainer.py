from levelgridwindow import *
from entityselectcontainer import *

#IDEA: allow right clicking on  level grid to remove objects.

class LevelEditorContainer(Box):
	def __init__(self,window,level_cell,dimensions):
		Box.__init__(self,dimensions[0],dimensions[1])
		self.master_window = window
		self.level_cell = level_cell
		
		level_name_label = Label(level_cell.get_name())
		print "Creating level grid window..."
		self.level_grid_window = self.level_grid_window() #this is the most time consuming part of opening the editor right now.
		print "Creating entity select container..."
		self.entity_select_container = self.entity_select_container(self.left+8,level_name_label.bottom+8,self.level_grid_window.left - 16,200)
		close_editor_button = self.close_editor_button(self.left + 8, self.bottom - 32) #also consider lower right corner
		
		self.add_child(level_name_label) #should be self if it can be altered, I think.
		self.add_child(self.level_grid_window)
		self.add_child(self.entity_select_container)#TEMP (object selection will mostly likely require more than one window.)
		self.add_child(close_editor_button)
		print "Level editor container created."
		print ""

	#TODO: label for the entity select container

	def entity_select_container(self,x,y,width,height):
		container = EntitySelectContainer(width,height) #may need "self" arg
		container.topleft = x,y
		return container

	def close_editor_button(self,x,y):
		button = Button("Close and Save")
		button.topleft = x,y
		button.connect_signal(SIG_CLICKED,self.closeEditor)
		return button

	def closeEditor(self):	#I sometimes have trouble making this work for some reason. (I think it happens if something is childless but needs children, like a window.)
		self.master_window.level_select_container.resume()
		self.master_window.destroy()

	def level_grid_window(self): #TODO: build from dungeon grid cells, not level data.
		level_cell = self.level_cell
		if level_cell.initialized():
			print "Creating level grid window for initialized level..."
			window = LevelGridWindow(self,self.left+400,self.top+8,360,360) 
			window.setGridData(level_cell)
			return window
		print "Creating level grid window for uninitialized level..."
		window = LevelGridWindow(self,self.left+400,self.top+8,360,360) 
		return window