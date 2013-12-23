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

	def dungeon_rooms(self,dungeon,dungeon_map):
		return RoomFactory.dungeon_rooms(dungeon,dungeon_map)

	def dungeon_levels(self,dungeon,rooms,level_data):
		levels = []
		#TODO:conisder making level_data its own class (to make this more extensible)
		for d in level_data:
			level_ID = d[0]
			origin = d[1]
			room_coords = d[2]
			level_rooms = []
			for c in room_coords: #TODO: error checking
				next_room = rooms[c[1]][c[0]]
				level_rooms.append(next_room)
			next_level = self.build_level(dungeon,level_ID,origin,level_rooms)
			levels.append(next_level)
		return levels

		#If I end up using the system where levelIDs are stored in arrays corresponding to rooms,
			#should probably have this done for dungeon in this method.
	def build_level(self,dungeon,level_ID,origin,rooms):
		return Level(dungeon,level_ID,origin,rooms)

		#might not end up using this
	def outdoors(self,depth,level_top):
		if(depth > 0): return False
		width = len(level_top)
		blocked = 0
		for t in level_top:
			if (t != " "): #should really be transparency check
				blocked += 1
		return blocked < width/1.5