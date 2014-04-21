"""This is currently the only class with a main method, so you can run the game from it.
currently the data for building the dungeon is read in from here, though that is likely to change as
the data gets more complicated."""

import gamescreen
from gamescreen import *
from dungeonfactory import *
from ocempgui import *

def runGame():
    """
    runGame () -> None

    Run the game with the dungeon saved in file 'dungeon0'. 
    Later, we might run the game with arguments to choose
    a particular dungeon.

    """
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    factory = DungeonFactory() #might need args like filename, filepath, etc later
    print "Building dungeon..."
    dungeon = factory.build_dungeon("./dungeon_map_files/dungeon0")
    print "Dungeon built."
    mainScreen = GameScreen()
    mainScreen.runGame(screen, dungeon)
    
if __name__ == "__main__":
    runGame()