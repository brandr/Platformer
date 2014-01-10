from levelgroup import *
import sys
sys.path.insert(0, './LevelEditor')
from filemanagercontainer import *
#TODO: import LevelEditor/dungeondata

class DungeonFactory(object):
	"""docstring for DungeonFactory"""
	def __init__(self):
		pass

		#returns a LevelGroup object by loading a dungeon file.
	def build_dungeon(self,filename):
		dungeon_data = FileManagerContainer.dungeonDataFromFile(filename)
		level_data_set = dungeon_data.level_data_set
		room_data_set = dungeon_data.rooms
		return LevelGroup(level_data_set,room_data_set) #could also give the factory itself more of the work than this