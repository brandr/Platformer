from leveleditorcontainer import *

LEVEL_WIN_WIDTH = 1000
LEVEL_WIN_HEIGHT = 650

class LevelEditorWindow(Window):
	def __init__(self,level_select_container,title,level_cell,position,dimensions):
		Window.__init__(self,title)
		self.level_select_container = level_select_container #need this to access click sensitivity
		self.topleft = (position[0],position[1])
		level_editor_container = LevelEditorContainer(self,level_cell,dimensions)
		self.set_child(level_editor_container)