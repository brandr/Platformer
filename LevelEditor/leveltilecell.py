from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from pygame import *

from tiledata import *

#LEVEL_TILE_WIDTH, LEVEL_TILE_HEIGHT = 32,32

#consider ImageMap instead of ImageLabel, maybe
class LevelTileCell(ImageLabel):
	"""docstring for LevelTileCell"""
	def __init__(self,tile_data = None):
		tile_image = Surface((32,32))
		tile_image.fill(Color("#FFFFFF"))
		self.tile_data = tile_data
		self.setTileImage(tile_data,tile_image)
		ImageLabel.__init__(self,tile_image) 
		self.padding = 1

	def setTileImage(self,tile_data,tile_image): #do we need tile_image as an arg? not sure
		if tile_data == None: return
		tile_image.blit(tile_data.get_image(),(0,0))