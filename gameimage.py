import os
from gameevent import *
from animationset import *

WIN_WIDTH = 800
WIN_HEIGHT = 640

BACKGROUND_COLOR = Color("#000000")
DEF_COLORKEY = Color("#FF00FF")

class GameImage(pygame.sprite.Sprite):
    def __init__(self, animations):
        pygame.sprite.Sprite.__init__(self)

        self.unseen_image = Surface((32,32))
        self.mapped = False
        self.animated = False #Temporary. this should probably be determined some other way (eg as a property of the animationSet itself)

        self.animation_set = animations
        self.animation = self.animation_set.default_animation()
        
        self.direction_id = 'default'
        self.animation_id = ('default', 'default')

        self.default_image = copy.copy(self.animation.images[0]) #this might be an inefficient/awkward place to use copy in the long run.
        self.image = self.default_image
        self.image.convert()
        self.rect = self.image.get_bounding_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def coordinates(self):
        return (self.rect.left/32, self.rect.top/32)

    def rect_coords(self):
        return (self.rect.left, self.rect.top)

    def moveTo(self, coords):
        self.moveRect(coords[0]*32, coords[1]*32, True)

    def moveRect(self, x_offset, y_offset, absolute = False):
        if(absolute):
            self.rect.left = x_offset
            self.rect.top = y_offset
            return
        self.rect.left += x_offset
        self.rect.top += y_offset

    def changeAnimation(self, ID, direction):
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
    def setLightLevel(image, light_value):
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
        self.image = self.unseen_image

    @staticmethod
    def still_animation_set(still_image, rect = Rect(0, 0, 32, 32), colorkey = DEF_COLORKEY):#colorkey = None):
        still_animation = SpriteStripAnimator(still_image, rect, 1, colorkey, False, 1)
        return AnimationSet(still_animation)

    @staticmethod
    def load_animation_set(tile_data, tile_size, colorkey = -1):
        image_pixel_width = tile_size*tile_data.width
        image_pixel_height = tile_size*tile_data.height
        image_rect = Rect(0, 0, image_pixel_width, image_pixel_height)

        key = tile_data.entity_key

        animation_keys = tile_data.animation_keys()
        if animation_keys == None: return None

        animation_filepath = tile_data.animation_filepath('./LevelEditor/')

        default_key = animation_keys[0][0]
        
        default_animation_filename = key + "_" + default_key + ".bmp"
        default_animation = GameImage.load_animation(animation_filepath, default_animation_filename, image_rect, colorkey)
        animation_set = AnimationSet(default_animation)
        
        for n in xrange(1, len(animation_keys)):
            anim_file_key = animation_keys[n][0]
            anim_key = animation_keys[n][1]
            anim_direction = animation_keys[n][2] 
            animation_filename = key + "_" + anim_file_key + ".bmp"
            next_animation = GameImage.load_animation(animation_filepath, animation_filename, image_rect, colorkey)
            #TODO: get the colorkey more generally (this may come up if we use animated blocks or square enemies).
            animation_set.insertAnimation(next_animation, anim_direction, anim_key)

        return animation_set

    @staticmethod
    def load_animation(filepath, filename, rect, colorkey = None, loop = True, frames = 10): #change frames to 50 if necessaryfor testing
        #animation_strip = GameImage.load_image_file(filepath, filename)
        animation_strip = GameImage.load_image_file("./animations", filename) #TEMP
        count = animation_strip.get_width()/rect.width #assume that the animation strip is wide only, not long
        return SpriteStripAnimator(animation_strip,rect, count, colorkey, loop, frames)

    @staticmethod
    def load_image_file(path, name, colorkey = None):
        fullname = os.path.join(path, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image