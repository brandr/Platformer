from levelgridwindow import *
from entityselectcontainer import *

#TODO: make it possible to set "outdoors".

class LevelEditorContainer(Box):
	def __init__(self,window,level_cell,dimensions):
		Box.__init__(self,dimensions[0],dimensions[1])
		self.master_window = window
		self.level_cell = level_cell
		
		level_name_label = Label(level_cell.get_name())

		self.level_grid_window = self.level_grid_window()
		
		self.entity_select_container = self.entity_select_container(self.left+8,level_name_label.bottom+8,self.level_grid_window.left - 16,360)
		
		
		self.sunlit = False #TODO: make sure sunlit is set correctly based on level cell's data.
		self.sunlit_button = CheckButton("Sunlit")
		self.sunlit_button.connect_signal(SIG_TOGGLED,self.toggleSunlit)
		self.sunlit_button.topleft = (self.entity_select_container.left,self.entity_select_container.bottom+8)
		self.setSunlit(level_cell.sunlit)
		#TODO: set sunlit button based on level cell.

		close_editor_button = self.close_editor_button(self.left + 8, self.bottom - 32) #also consider lower right corner

		self.add_child(level_name_label) #should be self if it can be altered, I think.
		self.add_child(self.level_grid_window)
		self.add_child(self.entity_select_container)
		self.add_child(self.sunlit_button)
		self.add_child(close_editor_button)

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
		self.level_cell.updateSunlit(self.sunlit)
		self.master_window.destroy()

	def level_grid_window(self):
		window = LevelGridWindow(self,self.left+400,self.top+8,360,360) 
		return window

	def setSunlit(self,sunlit):
		if(sunlit): self.sunlit_button.activate()

	def toggleSunlit(self):
		self.sunlit = not(self.sunlit)