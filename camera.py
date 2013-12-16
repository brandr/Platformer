import pygame
from pygame import Rect

WIN_WIDTH = 800
WIN_HEIGHT = 640

HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

CAMERA_SLACK = 30

global cameraX, cameraY

class Camera(object):
    def __init__(self, width, height):
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        camera = self.state
        
        l, t, _, _ = target.rect
        _, _, w, h = camera
        l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

        l = min(-64, l)                           # stop scrolling at the left edge (and hide part of it)
        l = max(-(camera.width-WIN_WIDTH)+64, l)   # stop scrolling at the right edge
        t = max(-(camera.height-WIN_HEIGHT)+64, t) # stop scrolling at the bottom
        t = min(-64, t) 
        self.state = Rect(l, t, w, h)
