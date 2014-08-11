#TODO: store cutscenes here

NEUTRAL = "neutral"

#MINER
MINER_BOSS_TEST_CUTSCENE = (	# TODO: figure out how to store this at a cutscene and parse it properly. 
								# right now it is stored as dialog, so dialog instructions need to specify that they are for dialogs and who should speak them.
	[
		("I am a boss character!", NEUTRAL),
		("I am going to fight you now!", NEUTRAL)
	],
	None # TODO: add some trigger to begin boss battle
)

MASTER_CUTSCENE_MAP = {
	"miner_boss_test_cutscene":MINER_BOSS_TEST_CUTSCENE
}