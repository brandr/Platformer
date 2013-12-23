import tilefactory
from tilefactory import *
import platformfactory
from platformfactory import *
import level
from level import *
import lantern
from lantern import *
import exitblock
from exitblock import *
import monster
from monster import *

class RoomFactory(object):

	@staticmethod
	def dungeon_rooms(dungeon,dungeon_map):
		ROOM_WIDTH = Room.ROOM_WIDTH
		ROOM_HEIGHT = Room.ROOM_HEIGHT
		rooms = []
		map_width = len(dungeon_map[0])
		map_height = len(dungeon_map)
		rooms_x = map_width/ROOM_WIDTH   #assuming evenly divisible right now
		rooms_y = map_height/ROOM_HEIGHT
		for y in range(0,rooms_y):	#NOTE: this for loop seems to obviate the need for global coords.
			rooms.append([])
			for x in range(0,rooms_x):
				next_room = RoomFactory.build_room(dungeon,dungeon_map,x,y)
				rooms[y].append(next_room)
		return rooms

	@staticmethod
	def build_room(dungeon,dungeon_map,global_x,global_y):
		tiles = []
		entities = [] #TODO: figure out why the original platformer used Group

		start_coords = (False,0,0)
		x = y = 0

		tile_images = GameImage.loadImageFile('test_tiles_1.bmp') 
		tile_factory = TileFactory(tile_images, (2,1))
		default_cave_tile = tile_factory.tile_at((0,0))
		default_sky_tile = tile_factory.tile_at((1,0))
		default_tile = default_cave_tile
		default_platform_image = GameImage.loadImageFile('testblock1.bmp')
		default_platform = GameImage.still_animation_set(default_platform_image)
		default_lantern = Lantern.load_lantern_animation_set()
		default_bat = Monster.load_bat_animation_set() 

		map_width = len(dungeon_map[0])
		map_height = len(dungeon_map)

		start_x = global_x*Room.ROOM_WIDTH
		start_y = global_y*Room.ROOM_HEIGHT

		end_x = min(start_x+Room.ROOM_WIDTH,map_width)
		end_y = min(start_y+Room.ROOM_HEIGHT,map_height)

		for row in range(start_y,end_y):
			tiles.append([])
			for col in range(start_x,end_x):
				t = Tile(default_tile, x,y)
				if dungeon_map[row][col] == "P":
					p = Platform(default_platform, x, y)
					entities.append(p)
					t.block = p
				if dungeon_map[row][col] == "L":
					l = Lantern(default_lantern, x, y, 2)
					entities.append(l)
				if dungeon_map[row][col] == "S":
					start_coords = (True,x,y)
				if dungeon_map[row][col] == "B":
					b = Monster(default_bat,"bat",x,y)
					entities.append(b)
				tiles[y/32].append(t)
				x += 32 
			y += 32
			x = 0

		room_objects = LevelObjects(None,tiles,entities)
		created_room = Room(room_objects,dungeon,(global_x,global_y),start_coords)
		return created_room