from tilefactory import *
from entityfactory import *
from signfactory import *
from doorfactory import *
from level import *

DEFAULT_SIGN = "default_sign"
DEFAULT_DOOR = "default_door"
NON_DEFAULT_ENTITY_MAP = {
	DEFAULT_SIGN:SignFactory,	# or a method in SignFactory?
	DEFAULT_DOOR:DoorFactory
}

class RoomFactory(object):

	@staticmethod
	def dungeon_rooms(dungeon, room_data_set):
		rooms = []
		x1, y1 = RoomFactory.origin(room_data_set)
		x2, y2 = RoomFactory.lower_right(room_data_set)
		print "Setting up rooms..."
		for y in range(y1, y2 + 1):	
			rooms.append([])
			for x in range(x1, x2 + 1):
				next_data = room_data_set[y][x]
				next_room = RoomFactory.build_room(dungeon, next_data, x, y)
				rooms[y].append(next_room)
		print "Rooms set up."
		return rooms

	@staticmethod
	def origin(room_data_set):
		for y in xrange(len(room_data_set)):
			for x in xrange(len(room_data_set[y])):
				next_data = room_data_set[y][x]
				if(room_data_set[y][x] != None): return x, y
		return None

	@staticmethod
	def lower_right(room_data_set):
		for y in range(len(room_data_set) - 1, -1, -1):
			for x in range(len(room_data_set[y]) - 1, -1, -1):
				next_data = room_data_set[y][x]
				if(room_data_set[y][x] != None): return x, y
		return None

	@staticmethod
	def build_room(dungeon, room_data, global_x, global_y): #might be able to get global x and global y through roomdata's coords instead
		if(room_data == None): return RoomFactory.empty_room(dungeon, global_x, global_y) 
		tiles = []
		entities = [] #TODO: figure out why the original platformer used Group

		start_coords = (False,0,0)
		x = y = 0

		#TODO: fix this part next
		tile_images = GameImage.load_image_file('./data/', 'test_tiles_1.bmp') 
		tile_factory = TileFactory(tile_images, (2,1))
		default_cave_tile = tile_factory.tile_at((0,0))
		default_tile = default_cave_tile

		end_x = ROOM_WIDTH
		end_y = ROOM_HEIGHT

		for row in xrange(end_y):
			tiles.append([])
			for col in xrange(end_x):
				next_tile_data = room_data.tile_at(col, row)
				t = Tile(default_tile, x, y)
				if next_tile_data != None and not isinstance(next_tile_data, BlockedTileData):
					if next_tile_data.entity_key == PLAYER_START:
						start_coords = (True, x, y)
					else:

						#TODO: remember that this part may need some checks if the object created is larger than 32*32.

						raw_entity_image = next_tile_data.get_image("./LevelEditor/")
						entity_width, entity_height = next_tile_data.width, next_tile_data.height
						entity_rect = Rect(0, 0, entity_width*DEFAULT_TILE_SIZE, entity_height*DEFAULT_TILE_SIZE)

						key = next_tile_data.entity_key
						if key in NON_DEFAULT_ENTITY_MAP:
							factory = NON_DEFAULT_ENTITY_MAP[key]
							entity = factory.build_entity(raw_entity_image, entity_rect, next_tile_data, x, y)
							entities.append(entity)
							if isinstance(entity, Block): 
								t.block = entity
						
						elif next_tile_data.is_animated():
							entity_animation_set = GameImage.load_animation_set(next_tile_data, DEFAULT_TILE_SIZE)
							e = EntityFactory.build_entity(entity_animation_set, key, x, y)
							entities.append(e)
		
						else:
							still_entity_image = GameImage.still_animation_set(raw_entity_image, entity_rect)
							e = EntityFactory.build_entity(still_entity_image, key, x, y)
							entities.append(e)
							if isinstance(e, Block): 
								t.block = e
		
				tiles[y/DEFAULT_TILE_SIZE].append(t)
				x += DEFAULT_TILE_SIZE 
			y += DEFAULT_TILE_SIZE
			x = 0
			
		room_objects = LevelObjects(None, tiles, entities)
		created_room = Room(room_objects, dungeon, (global_x, global_y), start_coords)
		return created_room

	@staticmethod
	def empty_room(dungeon, global_x, global_y):
		tiles = []
		entities = []

		start_coords = (False, 0, 0)
		x = y = 0

		tile_images = GameImage.load_image_file('./data/', 'test_tiles_1.bmp') 
		tile_factory = TileFactory(tile_images, (2, 1))
		default_cave_tile = tile_factory.tile_at((0, 0))
		default_sky_tile = tile_factory.tile_at((1, 0))
		default_tile = default_cave_tile

		end_x = ROOM_WIDTH
		end_y = ROOM_HEIGHT

		for row in xrange(end_y):
			tiles.append([])
			for col in xrange(end_x):
				t = Tile(default_tile, x, y)
				tiles[y/DEFAULT_TILE_SIZE].append(t)
				x += DEFAULT_TILE_SIZE 
			y += DEFAULT_TILE_SIZE
			x = 0

		room_objects = LevelObjects(None, tiles, entities)
		created_room = Room(room_objects, dungeon,(global_x, global_y), start_coords)
		return created_room