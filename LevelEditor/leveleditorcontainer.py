from levelgridwindow import *

class LevelEditorContainer(Box):
	def __init__(self,window,level_cell,dimensions):
		Box.__init__(self,dimensions[0],dimensions[1])
		self.master_window = window
		self.level_cell = level_cell
		
		self.level_grid_window = LevelGridWindow(self,self.left+200,self.top+8,400,400) #TODO: more args
		close_editor_button = self.close_editor_button(self.left + 8, self.bottom - 32) #also consider lower right corner
		
		self.add_child(self.level_grid_window)
		self.add_child(close_editor_button)

	def close_editor_button(self,x,y):
		button = Button("Close Editor")
		button.topleft = x,y
		button.connect_signal(SIG_CLICKED,self.closeEditor) #TODO (might need access to window)
		return button

	def closeEditor(self):	#I sometimes have trouble making this work for some reason. (I think it happens if something is childless but needs children, like a window.)
		self.master_window.level_select_container.resume()
		self.master_window.destroy()