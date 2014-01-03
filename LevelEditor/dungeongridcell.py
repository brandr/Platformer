from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

DUNGEON_CELL_WIDTH = 36
DUNGEON_CELL_HEIGHT = 36

class DungeonGridCell(Button):

	def __init__(self): #TODO: consider non-empty cells
		Button.__init__(self,"") #consider making this inherit from imagebutton rather than textbutton.
		self.minsize = DUNGEON_CELL_WIDTH,DUNGEON_CELL_HEIGHT
		self.connect_signal(SIG_CLICKED,self.test_click)

	def test_click(self): #temporary for testing
		self.set_text("O")
