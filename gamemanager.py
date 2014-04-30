""" A manager which controls the flow of gameplay, including switching between screens and controls.
"""

from screenmanager import *
from dungeonfactory import *
from cutscene import *

class GameManager:
	"""GameManager () -> GameManager

	This is the screen used to play the game.
	(Will add more description as more stuff is implemented.)

	Attributes: None
	"""
	def __init__(self):
		pass

	def run_game(self, master_screen):
		"""GM.runGame (...) -> None

		Run the game using a pygame screen.

		Attributes:
		master_screen: the pygame screen onto which everything will be displayed
		during the game.
		"""

		factory = DungeonFactory() #might need args like filename, filepath, etc later
		print "Building dungeon..."
		dungeon = factory.build_dungeon("./dungeon_map_files/dungeon0")
		print "Dungeon built."
		
		#old version for reference
		
		#mainScreen.runGame(master_screen, dungeon)

		#TODO: make what is below here work for the platformer.

		pygame.display.set_caption("title goes here")
		timer = pygame.time.Clock()

		player_animations = Player.load_player_animation_set()
		start_level = dungeon.start_level()
		
		player = Player(player_animations, start_level)
		start_level.addPlayer(player)

		game_controls = MainGameControls(player) #TODO: consider how controls may parse buttons differently for different screens.
		control_manager = ControlManager(game_controls)
		main_screen = MainGameScreen(control_manager, player) 
		screen_manager = ScreenManager(master_screen, main_screen, player)
		start_level.initialize_screen(screen_manager, main_screen)

		actors = [player]
		test_cutscene = Cutscene(actors)
		player.current_level.begin_cutscene(test_cutscene)

		while 1:
			timer.tick(90)

 			for e in pygame.event.get():
				screen_manager.process_event(e)
			screen_manager.update_current_screen()
			self.draw_screen(screen_manager)
			pygame.display.update()

	def draw_screen(self, screen_manager):
		screen_manager.draw_screen()