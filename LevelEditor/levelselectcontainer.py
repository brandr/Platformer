import levelselectcell
from levelselectcell import *
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

MAX_LEVELS = 99

class LevelSelectContainer(Box):
	def __init__(self,position,dimesions):
		Box.__init__(self,dimesions[0],dimesions[1])
		self.topleft = (position[0],position[1])

		self.level_count = 1

		level_select_label = Label("Dungeon Levels:")

		self.level_table = LevelSelectContainer.empty_level_table()
		self.level_table.topleft = (5,24)

		self.add_level_button = self.add_level_button() #TODO
		self.add_level_button.topleft = (5,48)

		self.add_child(level_select_label)
		self.add_child(self.level_table)
		self.add_child(self.add_level_button)


	def add_level_button(self):
		button = Button("Add a level")
		button.connect_signal (SIG_CLICKED, self.addLevel)
		#button.SIG_CLICKED = self.addLevel(added_level_name) #TEMP. TODO: try to do this bit witout actually calling the fuction.
		return button

	def addLevel(self):#,level_name):
		level_name = "level "+str(self.level_count)
		added_level_cell = LevelSelectCell(level_name)
		self.level_count += 1
		self.level_table.add_child(self.level_count,0,added_level_cell)
		#sel.
		#print "COUNT: "+str(self.level_count)

	@staticmethod
	def empty_level_table():
		table = Table (9, 1)
		table.spacing = 5
		table.topleft = 5, 5

		empty_cell = LevelSelectCell("level 0")
		table.add_child(0,0,empty_cell)		

		#label = Label ("Nonaligned wide Label")
		#table.add_child (0, 0, label)
		#table.add_child (0, 1, Button ("Simple Button"))

		#label = Label ("Top align")
		#table.add_child (1, 0, label)
		#table.set_align (1, 0, ALIGN_TOP)
		#table.add_child (1, 1, Button ("Simple Button"))

		return table

	
	#TODO 
	#@staticmethod
	#def level_select_cell():
	#	label = Label()