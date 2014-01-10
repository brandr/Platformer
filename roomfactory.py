from tilefactory import *
from platformfactory import *
from level import *
from lantern import *
from exitblock import *
from monster import *
import sys
sys.path.insert(0, './LevelEditor')
from roomdata import *

class RoomFactory(object):

	@staticmethod
	def dungeon_rooms(dungeon,room_data_set):
		#ROOM_WIDTH = Room.ROOM_WIDTH
		#ROOM_HEIGHT = Room.ROOM_HEIGHT
		rooms = []
		#map_width = len(room_data_set[0]) #might want to trim room_data_set before this point. (preferrably in the LevelEditor itself)
		#map_height = len(room_data_set)
		rooms_x = len(room_data_set[0])  #assuming evenly divisible right now
		rooms_y = len(room_data_set)
		for y in range(0,rooms_y):	#NOTE: this for loop seems to obviate the need for global coords.
			rooms.append([])
			for x in range(0,rooms_x):
				next_data = room_data_set[y][x]
				next_room = RoomFactory.build_room(dungeon,next_data,x,y)
				rooms[y].append(next_room)
		return rooms

	@staticmethod
	def build_room(dungeon,room_data,global_x,global_y): #might be able to get global x and global y through roomdata's coords instead
		if(room_data == None): return RoomFactory.empty_room(dungeon,global_x,global_y) 
		tiles = []
		entities = [] #TODO: figure out why the original platformer used Group

		start_coords = (False,0,0)
		x = y = 0
		#global_x,global_y = room_data.global_x,room_data.global_y #probably redundant

		tile_images = GameImage.loadImageFile('test_tiles_1.bmp') 
		tile_factory = TileFactory(tile_images, (2,1))
		default_cave_tile = tile_factory.tile_at((0,0))
		default_sky_tile = tile_factory.tile_at((1,0))
		default_tile = default_cave_tile
		default_platform_image = GameImage.loadImageFile('testblock1.bmp')
		default_platform = GameImage.still_animation_set(default_platform_image)
		default_lantern = Lantern.load_lantern_animation_set()
		default_bat = Monster.load_bat_animation_set() 

		end_x = ROOM_WIDTH
		end_y = ROOM_HEIGHT

		for row in xrange(end_y):
			tiles.append([])
			for col in xrange(end_x):
				next_tile_data = room_data.tile_at(col,row)
				t = Tile(default_tile, x,y)
				if next_tile_data != None:
				#TODO: think of a more extensible way to build these objects (probably through dictionaries or something)
					if next_tile_data.entity_key == DEFAULT_PLATFORM:
						p = Platform(default_platform, x, y)
						entities.append(p)
						t.block = p
					if next_tile_data.entity_key == PLAYER_START:
						start_coords = (True,x,y)
					if next_tile_data.entity_key == BAT:
						b = Monster(default_bat,"bat",x,y)
						entities.append(b)
				#if dungeon_map[row][col] == "L": #TODO: lantern
				#	l = Lantern(default_lantern, x, y, 2)
				#	entities.append(l)
				tiles[y/32].append(t)
				x += 32 
			y += 32
			x = 0

		room_objects = LevelObjects(None,tiles,entities)
		created_room = Room(room_objects,dungeon,(global_x,global_y),start_coords)
		return created_room

	@staticmethod
	def empty_room(dungeon,global_x,global_y):
		tiles = []
		entities = []

		start_coords = (False,0,0)
		x = y = 0

		tile_images = GameImage.loadImageFile('test_tiles_1.bmp') 
		tile_factory = TileFactory(tile_images, (2,1))
		default_cave_tile = tile_factory.tile_at((0,0))
		default_sky_tile = tile_factory.tile_at((1,0))
		default_tile = default_cave_tile

		end_x = ROOM_WIDTH
		end_y = ROOM_HEIGHT

		for row in xrange(end_y):
			tiles.append([])
			for col in xrange(end_x):
				t = Tile(default_tile, x,y)
				tiles[y/32].append(t)
				x += 32 
			y += 32
			x = 0

		room_objects = LevelObjects(None,tiles,entities)
		created_room = Room(room_objects,dungeon,(global_x,global_y),start_coords)
		return created_room