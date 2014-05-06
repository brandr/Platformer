"""This is the screen used to play the game."""

#TODO: divide what is in this screen into gamescreen (abstract) and maingamescreen (specfic)

from controlmanager import *
from player import *
from dungeon import *

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0

class GameScreen:
    """GameScreen () -> GameScreen

    This is the screen used to play the game.
    Later, it might be more useful to load the dungeon editor and the game from
    the same screen.

    Attributes: None
    """
    def __init__(self, control_manager): #not sure what other args should be yet.
        self.control_manager = control_manager
        self.screen_image = Surface((WIN_WIDTH, WIN_HEIGHT))

    def update(self):
        return None #TEMP

    def master_screen(self):
        return self.screen_manager.master_screen

    def draw_screen(self, master_screen):
        master_screen.blit(self.screen_image, (0, 0))
