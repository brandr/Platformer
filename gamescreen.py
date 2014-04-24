"""This is the screen used to play the game."""

from pygame import *
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
    def __init__(self):
        pass

    def runGame(self, screen, dungeon):
        """GS.runGame (...) -> None

        Run the game using a pygame screen and a dungeon built by a DungeonFactory.

        Currently keeps track of the player's controls and processes key presses in
        order to move the player around the screen. This method is also responsible
        for creating the player.

        """
        pygame.display.set_caption("title goes here")
        timer = pygame.time.Clock()

        bg = Surface((32, 32))
        bg.convert()
        bg.fill(BACKGROUND_COLOR)

        player_animations = Player.load_player_animation_set()
        
        start_level = dungeon.start_level()
        start_level.screen = screen
        player = Player(player_animations, start_level)
        start_level.addPlayer(player)

        # can probably make controls more extensible and put them in their own class.
        # could also make a dict instead of a series of if statements

        up = down = left = right = space = running = False #NOTE: rename running when I redesign the control system.
        while 1:
            timer.tick(110)
            for e in pygame.event.get():
                if e.type == QUIT: raise SystemExit, "QUIT"
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise SystemExit, "ESCAPE"

                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYDOWN and e.key == K_DOWN:
                    down = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                if e.type == KEYDOWN and e.key == K_LCTRL:
                    running = True
                if e.type == KEYDOWN and e.key == K_SPACE:
                    space = True

                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_DOWN:
                    down = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LCTRL:
                    running = False
                if e.type == KEYUP and e.key == K_SPACE:
                    space = False

        #draw background.
            #for y in range(32):
            #    for x in range(32):
            #        screen.blit(bg, (x * 32, y * 32))
            player.current_level.update(up, down, left, right, space, running)