from worldfilemanagercontainer import *
from dungeonselectcontainer import DungeonSelectContainer, LEFT_MOUSE_BUTTON
from startdataeditorcontainer import StartDataEditorContainer

#LEFT_MOUSE_BUTTON = 1
WORLD_WIN_WIDTH = 860	  
WORLD_WIN_HEIGHT = 540

class WorldEditorScreen:
	def __init__(self, world_renderer):
		self.world_renderer = world_renderer

	def openWorldEditor(self):
		self.initComponents()
		self.world_renderer.start()

	def initComponents(self):
		print "Intializing world editor components..."
		self.dungeon_select_container = self.dungeon_select_container(32, 32, 200, 400)
		self.file_manager_container = self.file_manager_container(self.dungeon_select_container, self.dungeon_select_container.right + 16, self.dungeon_select_container.top, 264, 400)
		self.start_data_editor_container = self.start_data_editor_container(self.file_manager_container.right + 16, self.file_manager_container.top, 300, 400)
		print "Dungeon editor components Intialized.", '\n'
		self.world_renderer.add_widget(self.dungeon_select_container)
		self.world_renderer.add_widget(self.file_manager_container)
		self.world_renderer.add_widget(self.start_data_editor_container)

	def dungeon_select_container(self, x, y, width, height):
		position = (x, y)
		dimensions = (width, height)
		return DungeonSelectContainer(position, dimensions)

	def file_manager_container(self, dungeon_select_container, x, y, width, height):
		position = (x, y)
		dimensions = (width, height)
		return WorldFileManagerContainer(dungeon_select_container, position, dimensions)

	def start_data_editor_container(self, x, y, width, height):
		position = (x, y)
		dimensions = (width, height)
		return StartDataEditorContainer(position, dimensions)
