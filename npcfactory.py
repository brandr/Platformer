""" A special factory for setting up NPCs.
"""

from nonplayercharacter import *
from tiledata import DEFAULT_NPC
from gameimage import GameImage
from animationset import AnimationSet
#NOTE: in the future, this may require saving/loading data
#about NPCs that appear in more than one area.

class NPCFactory:
	#TODO: make a bulid_entity method for default npcs and delete the corresponding code in init_NPC.

	@staticmethod
	def build_entity(raw_npc_image, npc_rect, npc_data, x, y):	#not sure if I can use sign_key-- might need a different structure to figure out the proper text
		""" build_entity( Surface, Rect, NPCData, int, int ) -> NonPlayerCharacter

		Take an npc image and rect to create the npc object that will appear on the level, and use the npc data 
		to build the text for the npc's dialogue.

		Note that the raw_npc_image is always the right-facing version, which will be algorithmically flipped to create the left-facing image.
		"""
		filepath = './animations/'
		file_key = npc_data.file_key
		npc_idle_left = GameImage.load_animation(filepath,  file_key + '_idle_left.bmp', npc_rect, -1)
		npc_idle_right = GameImage.load_animation(filepath,  file_key + '_idle_right.bmp', npc_rect, -1)
		animations = AnimationSet(npc_idle_left)
		animations.insertAnimation(npc_idle_left, 'left', 'idle')
		animations.insertAnimation(npc_idle_right, 'right', 'idle')
		npc = NonPlayerCharacter(animations, x, y)
		text_panes = npc_data.text_panes
		dialog_set = [] 		
		for t in text_panes: 
			text = ""
			for line in t:
				text += line
			dialog_set.append( ( text, None ) )
		npc.dialog_tree = ( dialog_set, None )
		npc.dialog_tree_map = { START: npc.dialog_tree }
		#sign.set_text_set(sign_text_panes)		# TODO: need to build a dialog tree instead of using set_text_set.
		return npc

	@staticmethod
	def init_NPC(npc, name):
		""" init_NPC( NonPlayerCharacter, str ) -> None

		Temporary method which initializes the NPC's dialog tree and name.
		I'm not sure how I want dialog trees to be stored and assigned to NPCs.
		They shouldn't have to be too complex, so it might be possible to just hardcode them.
		"""
		npc.name = name

		#TEMP FOR TESTING
		if name in MASTER_NPC_DIALOG_MAP[COMPLEX]:
			temp_dialog_tree_map = MASTER_NPC_DIALOG_MAP[COMPLEX][name] 
		# TODO: need to make dialog more extensible later on
		# IDEA: map each NPC by name to a dict of possible dialogs, whose key (or value?) can in turn be changed somehow.
		#TEMP FOR TESTING
			npc.dialog_tree = temp_dialog_tree_map[START] # later on, it might be useful to change START to some value that can change as the game progresses.
			npc.dialog_tree_map = temp_dialog_tree_map
		elif name == DEFAULT_NPC:
			print "SIMPLE HUMAN"
			#TODO: treat the NPC's dialogue exactly like a sign's

START = "start"
COMPLEX = "complex"
SIMPLE = "simple"
TEST_KENSTAR_TIRED = "test_kenstar_tired"

# for now, test dialog trees go here.

#MINER
TEST_MINER_DIALOG_TREE = (	# TODO: figure out how to store this at a cutscene and parse it properly
	[
		("I am a boss character!", NEUTRAL),
		("I am going to fight you now!", NEUTRAL)
	],
	None #TODO: add some trigger to begin boss battle
)

#KENSTAR
TEST_KENSTAR_START_DIALOG_TREE = (
	[
		("Whaaaaaaaaaaat is this place??", NEUTRAL),
		("It looks like some kind of... demo.", NEUTRAL)
	],
	(
		DIALOG_CHOICE,
		("Do you know the way out of here?", NEUTRAL),
		[ 
			("Yes", 
				[
					("Whoa, really?", NEUTRAL)
				],
				(
					DIALOG_CHOICE,
					("Is it to the right?", NEUTRAL),
					[
						("Yes",
							[
								("Well, then, I'd better get going!", NEUTRAL),
								("...and by that, I mean walk slightly to the right.", NEUTRAL)		
							],
							(
								ACTION_SET,
								[ 
									(	#TODO: make the action work
										NonPlayerCharacter.temp_npc_right_method, 30, None 
									),
									(
										NonPlayerCharacter.temp_stop_method, 0, None 
									)
								],
								(
									ADD_DIALOG_SET,
									[
										("That's enough walking for one day.", NEUTRAL)
									], 
									(
										SETUP_NEXT_DIALOG,
										TEST_KENSTAR_TIRED
									)
								), None
							)
						),
						("No",
							[
								("I don't belive you! I came from that direction!", NEUTRAL)
							], None
						)
					]
				)
			),
			("No", 
				[
					("Well, let me know if you find it.", NEUTRAL)
				], None
			)
		]
	)
)

TEST_KENSTAR_TIRED_DIALOG_TREE = (
	[
		("Boy, I sure am tired.", NEUTRAL)
	], None
)

TEST_KENSTAR_DIALOG_TREE_MAP = {
	START:TEST_KENSTAR_START_DIALOG_TREE,
	TEST_KENSTAR_TIRED:TEST_KENSTAR_TIRED_DIALOG_TREE
}

TEST_MINER_DIALOG_TREE_MAP = {
	START:TEST_MINER_DIALOG_TREE
}

MASTER_NPC_DIALOG_MAP = {
	COMPLEX:{
		KENSTAR:TEST_KENSTAR_DIALOG_TREE_MAP,
		MINER:TEST_MINER_DIALOG_TREE_MAP
	}
}