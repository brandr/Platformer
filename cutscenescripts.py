#TODO: store cutscenes here

# UNIQUE ACTOR KEYS
PLAYER = "player"
MINER = "miner"	 # Can the "world" be an actor? can there be no actor?

# ACTION KEYS
BEGIN_DIALOG_TREE = "dialog_tree"

# DIALOG EXPRESSION KEYS
NEUTRAL = "neutral"

#MINER
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

MASTER_CUTSCENE_MAP = {
	"miner_boss_test_cutscene":MINER_BOSS_TEST_CUTSCENE
}