from platformfactory import *
from ladder import *
from sign import *
from lantern import *
from exitblock import *
from monster import *
from roomdata import *

ENTITY_CONSTRUCTOR_MAP = {
	DEFAULT_PLATFORM:Platform,
	SLOPING_PLATFORM:Platform,

	DEFAULT_LADDER:Ladder,

	DEFAULT_SIGN:Sign,

	DEFAULT_LANTERN:Lantern,
	
	BAT:Monster,
	GIANT_FROG:Monster
}

class EntityFactory(object):

	@staticmethod
	def build_entity(animation_set, entity_key, x, y):
		if entity_key not in ENTITY_CONSTRUCTOR_MAP: return None
		constructor = ENTITY_CONSTRUCTOR_MAP[entity_key]
		entity = constructor(animation_set, x, y)
		if entity_key in ENTITY_BUILD_MAP:
			build_function = ENTITY_BUILD_MAP[entity_key]
			build_function(entity, entity_key)
		return entity

	#add other monster init stuff as necessary.
	@staticmethod
	def initMonster(monster, name):
		monster.name = name

	@staticmethod
	def initSlopingPlatform(platform, arg):
		platform.is_sloped = True
		platform.is_sloped = False

ENTITY_BUILD_MAP = {
	SLOPING_PLATFORM:EntityFactory.initSlopingPlatform,
	BAT:EntityFactory.initMonster,
	GIANT_FROG:EntityFactory.initMonster
}