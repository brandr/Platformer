""" A set of levels that exist on a grid, where each grid square represents a single room and a level may be one or more rooms.
"""

import levelfactory
from levelfactory import *
import player
from player import *

# Dungeon currently represents all the levels in the game. If for some reason it becomes undesirable
# to store all levels in one Dungeon, (example: the game takes too long to load, the level arrangements we want don't
# fit neatly into one grid, etc) then we might make it possible to travel between LevelGroups.

class Dungeon(object):
	""" Dungeon( [ LevelData ], [ [ RoomData ] ] ) -> Dungeon

	A dungeon is effectively a set of levels. Functionally, the rooms are not processed individually after the dungeon is created--
	instead, the player's current level is constantly updated and is connected to other levels.

	Attributes: 

	rooms: The set of square, same-sized rooms that make up the dungeon.

	dungeon_levels: The set of levels (each containing one or more rooms) that make up the dungeon.
	"""
	def __init__(self, level_data_set, room_data_set): #Dungeon builds the dungeon from a single map along with some other data about the level.
		factory = LevelFactory()
		print "Building dungeon rooms..."
		rooms = factory.dungeon_rooms(self, room_data_set)
		self.dungeon_levels = factory.dungeon_levels(self, rooms, level_data_set)
		for L in self.dungeon_levels:
			L.calibrateExits() #needed in case there are ways out of levels that don't lead to other levels.
		
	def start_level(self):
		""" d.start_level( ) -> Level 

		The level where the player starts the game. Might want to change this system if the player can
		travel between dungeons, save the game, etc.
		"""
		for L in self.dungeon_levels:
			if(L.start_coords != None):
				return L
		return None

		#TODO: error case where next_level is None.
	def movePlayer(self, screen_manager, screen, player, next_level, global_coords, local_coords):
		""" d.movePlayer( ScreenManager, GameScreen, Playr, Level, (int, int), (int, int) ):

		Moves the player to another level at the appropriate position based on the level the player is leaving.
		"""
		room_coords = (local_coords[0]%ROOM_WIDTH,local_coords[1]%ROOM_HEIGHT)
		next_coords = next_level.flipped_coords(global_coords, room_coords) #TODO: will have to change this
		next_level.screen_manager = screen_manager
		next_level.screen = screen
		next_level.addPlayer(player, next_coords)
		
	def level_at(self, x, y):
		""" d.level_at( int, int ) -> Level

		Returns the level at the given coordinates in the dungeon.
		Note that these coordinates techincally point to a room, so the returned level is techincally
		the one containing that room.
		"""
		for L in self.dungeon_levels:
			global_coords = L.origin
			level_end = L.level_end_coords()
			if(global_coords[0] <= x <= level_end[0] and global_coords[1] <= y <= level_end[1]):
				return L
		return None