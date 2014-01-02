from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

class LevelSelectCell(Table):
	def __init__(self,name):#TODO: args specific to LevelSelectCells 
		Table.__init__(self,1,3)
		#self.name = name	#TODO:specify which level (consider retrieving frm self.level_data)
		name_label = Label(name)
		self.add_child(0,0,name_label)
		#self.addText("Level 1:",22,DEFAULT_MARGIN/8,DEFAULT_MARGIN/8) #TODO: consider 
		#self.level_data = None		#TODO: a new level select cell should create a new levelData data member (have to define this class)
		#self.initializeButtons()
