from platformfactory import *
from lantern import *
from exitblock import *
from monster import *
#import sys
#sys.path.insert(0, '.\LevelEditor')
from roomdata import *

ENTITY_CONSTRUCTOR_MAP = {
	DEFAULT_PLATFORM:Platform,
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

ENTITY_BUILD_MAP = {
	BAT:EntityFactory.initMonster,
	GIANT_FROG:EntityFactory.initMonster
}