"""This is currently the only class with a main method, so you can run the game from it.
currently the data for building the dungeon is dealt with by GameManager."""

from gamemanager import *

def runGame():
    """
    runGame () -> None

    Run the game using whatever default starting conditions are set in GameManager.
    """
    pygame.init()
    manager = GameManager()
    manager.run_game()

if __name__ == "__main__":
    runGame()