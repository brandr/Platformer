from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from pygame import *

LEVEL_TILE_WIDTH, LEVEL_TILE_HEIGHT = 32,32

#consider ImageMap instead of ImageLabel, maybe
class LevelTileCell(ImageLabel):
	"""docstring for LevelTileCell"""
	def __init__(self):
		blank_square = Surface((32,32))
		blank_square.fill(Color("#FFFFFF"))
		#TODO: make it possible to store, change, and update image. 
		#image should probably be retrieved from some other object, and maybe blitted against the white square.
		ImageLabel.__init__(self,blank_square) #going with a imagelabel for now, though we might want something else.
		self.padding = 1