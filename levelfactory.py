import roomfactory
from roomfactory import *

#The LevelFactory calls methods from RoomFactory (along with some additional methods)
	#to create the dungeon levels based on a set of input.

class LevelFactory(object):

	def __init__(self):
		#neither of these are used right now. Might make LevelFactory a static class if it needs no private data.
		self.global_x = 0
		self.global_y = 0

	#maybe this should go in roomfactory instead

	#new  dungeon_rooms method
	def dungeon_rooms(self, dungeon, room_data_set):
		return RoomFactory.dungeon_rooms(dungeon, room_data_set)

	def dungeon_levels(self, dungeon, rooms, level_data_set):
		levels = []
		for d in level_data_set:
			level_rooms = d.room_set(rooms)
			origin = d.corners[0]
			next_level = self.build_level(dungeon,d,origin,level_rooms)
			levels.append(next_level)
		return levels

		#If I end up using the system where levelIDs are stored in arrays corresponding to rooms,
			#should probably have this done for dungeon in this method.
	def build_level(self, dungeon, level_data, origin, rooms): #could also get orgin from level data
		return Level(dungeon, level_data, origin, rooms)

		#might not end up using this
	def outdoors(self, depth, level_top):
		if(depth > 0): return False
		width = len(level_top)
		blocked = 0
		for t in level_top:
			if (t != " "): #should really be transparency check
				blocked += 1
		return blocked < width/1.5