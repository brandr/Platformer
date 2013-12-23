import levelfactory
from levelfactory import *
import player
from player import *

#LevelGroup currently represents all the levels in the game. If for some reason it becomes undesirable
	#to store all levels in one levelGroup, (example: the game takes too long to load, the level arrangements we want don't
    #fit neatly into one grid, etc) then we might make it possible to travel between LevelGroups.

class LevelGroup(object):
	def __init__(self,dungeon_map,level_data): #levelGroup builds the dungeon from a single map (currently ascii) along with some other data about the level.
		factory = LevelFactory()
		self.rooms = factory.dungeon_rooms(self,dungeon_map) #maybe this should be done by a room factory instead of a level factory
		self.dungeon_levels = factory.dungeon_levels(self,self.rooms,level_data)
		for L in self.dungeon_levels:
			L.calibrateExits() #needed in case there are ways out of levels that don't lead to other levels.

	#level where the player starts the game
	def start_level(self):
		for L in self.dungeon_levels:
			if(L.start_coords != None):
				return L
		return None

		#TODO: error case where next_level is None.
	def movePlayer(self,player,next_level,global_coords,local_coords):
		room_coords = (local_coords[0]%Room.ROOM_WIDTH,local_coords[1]%Room.ROOM_HEIGHT)
		next_coords = next_level.flipped_coords(global_coords,room_coords) #TODO: will have to change this
		next_level.addPlayer(player,next_coords)
		
	def level_at(self,x,y):
		for L in self.dungeon_levels:
			global_coords = L.origin
			level_end = L.level_end_coords()
			if(global_coords[0]<=x<=level_end[0] and global_coords[1]<=y<=level_end[1]):
				return L
		return None