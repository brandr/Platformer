import levelselectcontainer
from levelselectcontainer import *
import dungeongridcontainer
from dungeongridcontainer import *
#TODO: dungeongridcontainer
import pygame
from pygame import *
from ocempgui.widgets import *

#TODO: make the level select container a scrollable window instead.

WIN_WIDTH = 800
WIN_HEIGHT = 540

class DungeonEditorScreen(object):
	def __init__(self,renderer):
		self.renderer = renderer

	def openEditor(self):
		self.initComponents(self.renderer)
		self.renderer.start()

	def initComponents(self,renderer): #could maybe be static

		level_select_container = DungeonEditorScreen.level_select_container(32,32,312,360)
		dungeon_grid_container = DungeonEditorScreen.dungeon_grid_container(level_select_container.right+36,level_select_container.top,312,360)
		#TODO: anything else the leveleditor might need

		self.renderer.add_widget(level_select_container)
		self.renderer.add_widget(dungeon_grid_container)

	#def notify(self,event):
	#	if(event.signal != "entered"):
	#		print event.signal
	#		print event.data

	@staticmethod
	def level_select_container(pos_x,pos_y,width,height):
		position = (pos_x,pos_y)
		dimensions = (width,height)
		return LevelSelectContainer(position,dimensions)

	@staticmethod
	def dungeon_grid_container(pos_x,pos_y,width,height):
		position = (pos_x,pos_y)
		dimensions = (width,height)
		return DungeonGridContainer(position,dimensions)