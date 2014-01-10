import gamescreen
from gamescreen import *
from dungeonfactory import *

#PLATFORMEXAMPLE (name will probably change):
    #this is currently the only class with a main method, so you can run the game from it.
    #currently the data for building the dungeon is read in from here, though that is likely to change as
        #the data gets more complicated.

def runGame():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)

    #new way of creating a dungeon (works for now)
    factory = DungeonFactory() #might need args like filename, filepath, etc later
    dungeon = factory.build_dungeon("./LevelEditor/dungeon_map_files/dungeon0")
    
    #uncomment these to test actually launching the dungeon
    mainScreen = GameScreen()
    mainScreen.runGame(screen,dungeon)
    
if __name__ == "__main__":
    runGame()