import levelselectcontainer
from levelselectcontainer import *
import pygame
from pygame import *
from ocempgui.widgets import *

#TODO: make the level select container a scrollable window instead.

WIN_WIDTH = 800
WIN_HEIGHT = 640

class DungeonEditorScreen(object):
	def __init__(self,renderer):
		self.renderer = renderer

	def openEditor(self):
		self.initComponents(self.renderer)
		self.renderer.start()

	def initComponents(self,renderer): #could maybe be static

		level_select_container = DungeonEditorScreen.level_select_container()
		#level_table = DungeonEditorScreen.empty_level_table()
		#TODO: dungeon grid, other stuff

		#TODO: level table
		self.renderer.add_widget(level_select_container)

	@staticmethod
	def level_select_container():
		position = (32,32)
		dimensions = (312,360)
		return LevelSelectContainer(position,dimensions)