import pygame
from pygame import *
import numpy
from numpy import *
import player
from player import *
import levelgroup
from levelgroup import *

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0

class GameScreen:
    def __init__(self):
        pass

    def runGame(self,screen,levels):

        pygame.display.set_caption("title goes here")
        timer = pygame.time.Clock()

        bg = Surface((32,32))
        bg.convert()
        bg.fill(BACKGROUND_COLOR)

        #probably should replace this with an animationset
        player_animations = Player.load_player_animation_set()
        
        start_level = levels.start_level()
        player = Player(player_animations,start_level)
        start_level.addPlayer(player)

        up = down = left = right = running = False
        while 1:
            timer.tick(100)
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
                if e.type == USEREVENT + 1: #NOTE: this is not very extensible. it is a quick fix only
                   player.mobilize()
        # draw background
            for y in range(32):
                for x in range(32):
                    screen.blit(bg, (x * 32, y * 32))
            #print player.current_level.level_ID
            player.current_level.update(screen,up, down, left, right, running)