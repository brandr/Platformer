from ocempgui.widgets import *
from ocempgui.widgets.Constants import *


class LevelEditorContainer(Box):
	def __init__(self,window,level_cell,dimensions):
		Box.__init__(self,dimensions[0],dimensions[1])
		self.window = window
		close_editor_button = self.close_editor_button(self.left + 32, self.bottom - 32)
		self.add_child(close_editor_button)

	def close_editor_button(self,x,y):
		button = Button("Close Editor")
		button.topleft = x,y
		button.connect_signal(SIG_CLICKED,self.closeEditor) #TODO (might need access to window)
		return button

	def closeEditor(self):
		self.window.level_select_container.resume()
		self.window.destroy()