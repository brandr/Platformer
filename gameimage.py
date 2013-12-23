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
        #self.unseen_color = Color("#000000")\
        self.unseen_image = Surface((32,32))
        self.mapped = False
        self.animated = False #Temporary. this should probably be determined some other way (eg as a property of the animationSet itself)

        self.animation_set = animations
        self.animation = self.animation_set.default_animation()
        
        self.direction_id = 'default'
        self.animation_id = ('default','default')

        self.default_image = copy.copy(self.animation.images[0]) #this might be an inefficient/awkward place to use copy in the long run.
        self.image = self.default_image
        self.image.convert()
        self.rect = self.image.get_bounding_rect()

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

    def coordinates(self):
        return (self.rect.centerx/32,self.rect.centery/32)

    def rect_coords(self):
        return (self.rect.left,self.rect.top)

    def moveTo(self, coords):
        self.moveRect(coords[0]*32,coords[1]*32,True)

    def moveRect(self,x_offset,y_offset,absolute = False):
        if(absolute):
            self.rect.centerx = x_offset
            self.rect.centery = y_offset
            return
        self.rect.centerx += x_offset
        self.rect.centery += y_offset

    def changeAnimation(self, ID,direction):
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
        
        if(lightvalue != 0): 
            if(self.default_image != None):
                self.image = self.default_image
            self.image.set_alpha(lightvalue)
        else: 
            if(self.mapped):
                self.fully_darken()
                return
            #self.image = Surface((32, 32))
            #self.image.fill(BACKGROUND_COLOR) 

    def updateAnimation(self, lightvalue = 0):
        if(self.animated):
            self.animate()
            #not sure how best  to process lightvalue at this point.
            #GameImage.setLightLevel(self.image,lightvalue)
            #self.image.set_alpha(lightvalue)
            return
        self.updateimage(lightvalue)

    #def map_image(self,unseen_color = Color("#000000")):
    #    if(self.mapped): return
    #    self.mapped = True
    #    self.unseen_color = unseen_color

    @staticmethod
    def setLightLevel(image,light_value):
        light_value = 255
        dark = pygame.Surface(image.get_size(), 32)
        dark.set_alpha(light_value, pygame.RLEACCEL)
        image.blit(dark, (0, 0))

    def animate(self):
        self.image = self.animation.next()

    def darkenTo(self, lightvalue):
        current_lightvalue = self.image.get_alpha()
        self.image.set_alpha(min(current_lightvalue, lightvalue))

    def check_brightness(self):
        brightness = self.image.get_alpha()
        if(brightness == None):
            return 0
        return brightness

    def fully_darken(self):
        self.image = self.unseen_image#Surface((32, 32))
        #self.image.fill(self.unseen_color)