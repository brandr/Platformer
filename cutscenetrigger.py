""" An invisible trigger that will cause a cutscene to play if the player comes into contact with it and hasn't seen the cutscene yet.
"""

from block import *
from cutscenescripts import MASTER_CUTSCENE_MAP
from cutscene import Cutscene
from gameaction import GameAction

class CutsceneTrigger(Block):
	""" CutsceneTrigger( AnimationSet, int, int ) -> CutsceneTrigger

	TODO

	Attributes:

	cutscene_key: A string key uniquely associating this trigger with some cutscene.
	"""
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.x_interactable = False
		self.is_solid = False
		self.cutscene_key = None

	def update(self, player):
		""" ct.update( Player ) -> None

		Check if the player has collided with this trigger (and not activated the cutscene yet).
		If the cutscene has already been activated, delete this trigger.
		"""
		if player.has_viewed_cutscene(self.cutscene_key):
			self.delete()
			return
		if pygame.sprite.collide_rect(self, player) and self.cutscene_key:
			self.begin_cutscene(player)

	def begin_cutscene(self, player):
		""" ct.begin_cutscene( Player ) -> None

		Build the cutscene associated with this trigger and make the player watch it.
		"""
		level = player.current_level
		cutscene_script = MASTER_CUTSCENE_MAP[self.cutscene_key]
		cutscene_action_data_list = cutscene_script[0]
		start_action_list = self.build_cutscene_action_list(cutscene_action_data_list, level)
		cutscene = Cutscene(start_action_list)
		level.begin_cutscene(cutscene)
		#TODO: parse "cutscene syntax" for any case, extensibly
		player.viewed_cutscene_keys.append(self.cutscene_key)

	def build_cutscene_action_list(self, action_data_list, level):
		""" ct.build_cutscene_action_list( [ ? ], Level ) -> [ GameAction ]

		Parse a set of primitive action_data into a list of start GameActions (to be executed simultaneously).
		"""
		start_action_list = []
		for d in action_data_list:
			action = self.build_action(d, level)
			start_action_list.append(action)
		return start_action_list

	def build_action(action_data, level):
		""" ct.build_action( ?, Level ) -> GameAction

		TODO
		"""
		#TODO: figure out what is required to begin a dialog tree
		action_key = action_data[1]
		actor_key = action_data[0]
		arg = ?
		duration = ?
		method = ?		
		action = GameAction(method, duration, actor, arg)
		#TODO: add next actions
		return action

# example cutscene data
"""
MINER_BOSS_TEST_CUTSCENE = (	# TODO: figure out how to store this at a cutscene and parse it properly. Write up "cutscene syntax" somewhere. (Incorporate dialog syntax)
								# right now it is stored as dialog, so dialog instructions need to specify that they are for dialogs and who should speak them.
	[
		(
			MINER,
			BEGIN_DIALOG_TREE,
			(
				[
					("I am a boss character!", NEUTRAL),
					("I am going to fight you now!", NEUTRAL)
				], 
				None
			)
		)
		
	], None # TODO: add some trigger to begin boss battle at the end of the cutscene
)
"""