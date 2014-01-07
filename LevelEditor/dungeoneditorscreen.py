import levelselectcontainer
from levelselectcontainer import *
import dungeongridcontainer
from dungeongridcontainer import *
import pygame
from leveleditorscreen import *

DUNGEON_WIN_WIDTH = LEVEL_WIN_WIDTH	  #TEMP (maybe?)
DUNGEON_WIN_HEIGHT = LEVEL_WIN_HEIGHT #TEMP

class DungeonEditorScreen(object):
	def __init__(self,dungeon_renderer):#,level_renderer):
		self.dungeon_renderer = dungeon_renderer

	def openDungeonEditor(self):
		self.initComponents()
		self.dungeon_renderer.start()

	def initComponents(self):#,renderer): #could maybe be static

		level_select_container = self.level_select_container(32,32,312,428)
		dungeon_grid_container = self.dungeon_grid_container(level_select_container,level_select_container.right+36,level_select_container.top,312,360)
		#TODO: anything else the dungeoneditor might need (consider buttons for saving and loading here)

		self.dungeon_renderer.add_widget(level_select_container)
		self.dungeon_renderer.add_widget(dungeon_grid_container)

		#I forget if we're still using this method.
	def openLevelEditor(self,level_cell): #consider making this pass some object held by the LevelSelectCell instead, if that's simpler.
		#TODO: figure out what data/updates will need to pass betweent the dungeon and level editors.
		level_renderer = Renderer()
		level_renderer.screen = self.dungeon_renderer.screen
		level_renderer.title = "Level Editor"
		level_renderer.color = (250,250,250)
		
		level_editor_screen = LevelEditorScreen(self,level_renderer)#,level_renderer)
		level_editor_screen.openLevelEditor() #add more args if necessary

	def level_select_container(self,x,y,width,height):
		position = (x,y)
		dimensions = (width,height)
		return LevelSelectContainer(self,position,dimensions)

	def dungeon_grid_container(self,level_select_container,pos_x,pos_y,width,height):
		position = (pos_x,pos_y)
		dimensions = (width,height)
		return DungeonGridContainer(level_select_container,position,dimensions)