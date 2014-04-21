from dungeon import *
import sys
import json
from dungeondata import *

class DungeonFactory(object):
	"""docstring for DungeonFactory"""
	def __init__(self):
		pass

		#returns a LevelGroup object by loading a dungeon file.
	def build_dungeon(self, filename):
		dungeon_data = DungeonFactory.dungeonDataFromFile(filename)
		level_data_set = dungeon_data.level_data_set
		room_data_set = dungeon_data.rooms
		print "Setting up main level group..."
		return Dungeon(level_data_set,room_data_set) #could also give the factory itself more of the work than this

	@staticmethod
	def dungeonDataFromFile(filename, filepath = "./"):
		dungeon_file = open(filename,'rb') #'rb' means "read binary"
		dungeon_data = json.load(dungeon_file) #this part reads the data from file
		deformatted_dungeon = DungeonData.deformatted_dungeon(dungeon_data,filepath)
		return deformatted_dungeon