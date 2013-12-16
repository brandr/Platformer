import os, pygame
from pygame import *
import animationset
from animationset import *

BACKGROUND_COLOR = Color("#000000")

#consider an animation_data arg which determines # of animations and # of frames/duration in each.
#alternately, consider taking animationSet as an arg.
class GameImage(pygame.sprite.Sprite):
    def __init__(self,animations):#,default_rect,colorkey = None):#,start_coords):
        pygame.sprite.Sprite.__init__(self)
        self.unseen_color = Color("#000000")
        self.mapped = False
        self.animated = False #Temporary. this should probably be determined some other way (eg as a property of the animationSet itself)

        self.animation_set = animations
        self.animation = self.animation_set.default_animation()
        self.animation_id = ('default','default')

        self.default_image = copy.copy(self.animation.images[0]) #this might be an inefficient/awkward place to use copy in the long run.
        self.image = self.default_image
        self.image.convert()
        self.rect = self.image.get_rect()

    @staticmethod
    def loadImageFile(name,colorkey = None):
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image

    @staticmethod
    def load_animation(filename, rect, count, colorkey=None, loop=True, frames=10): #change to 50 if necessaryfor testing
        animation_strip = GameImage.loadImageFile(filename)
        return SpriteStripAnimator(animation_strip,rect, count, colorkey, loop, frames)

    @staticmethod
    def still_animation_set(still_image, rect = Rect(0,0,32,32), colorkey = None):
        still_animation = SpriteStripAnimator(still_image,rect, 1, colorkey, False, 1)
        return AnimationSet(still_animation)

    def changeAnimation(self, ID='default',direction = None):
        #if(ID == 'running'): print ID + ", " + str(self.animation_id)
        if(self.animation_id[0] == (ID)):
            if(direction == None or self.animation_id[1] == direction):
               return
        if(direction != None):
            self.changeDirection(direction) 
        self.animation = self.direction_set[ID]
        self.animation.iter()
        self.animation_id = (ID,direction)

    def changeDirection(self, direction):
        self.direction_set = self.animation_set.set_in_direction(direction) 

    def updateimage(self, lightvalue = 0):
        if(self.animated):
            self.animate()
            return
        if(lightvalue != 0): 
            if(self.default_image != None):
                self.image = self.default_image
            self.image.set_alpha(lightvalue)
        else: 
            if(self.mapped):
                self.fully_darken()
                return
            self.image = Surface((32, 32))
            self.image.fill(BACKGROUND_COLOR)  #TODO: eventually split into cases for "mapped" and "not mapped" (plan ahead)

    def animate(self):
        #self.animation.iter()
        self.image = self.animation.next()

    def darkenTo(self, lightvalue):
        current_lightvalue = self.image.get_alpha()
        self.image.set_alpha(min(current_lightvalue, lightvalue))

    def check_brightness(self):
        return self.image.get_alpha()

    def fully_darken(self):
        self.image = Surface((32, 32))
        self.image.fill(self.unseen_color)