"""Represents something more specific than an entity or gameImage, but less specific than
a block or monster. A being is an entity that does not occupy a specific tile 
(like a block/platform does). Beings can be stationary, though they almost always move.
"""

from entity import *
from platform import *

class Being(Entity):
    """ Being ( animations ) -> Being

    A Being is initialized the same as its supeclass, Entity, but it is still an abstract class
    that can be used for monsters, the player, moving traps, or anything else that affects 
    gameplay but isn't bound to a specific tile.

    The xvel and yvel attributes represent the being's current x and y velocities (where a positive
    xvel makes the Being move right and a positive yvel moves it down).

    The onGround attribute says whether the being is on the ground, and is useful for jumping methods.

    Running says whether the being is currently running. Currently this is only applicable to the player,
    so it might need to be renamed to be more general or moved to the player class.

    Sightdist represents the Being's vision radius in tiles. For the player, it determines the radius of 
    lit tiles around the player, and for monsters, it should determine how far away they can see the player
    from.

    max_speed determines the fastest speed the Being can travel in any direction.

    bounce_count represents the remaining time that the Being is "bouncing" for. Generally, no Being can
    change direction while it's bouncing.
    """

    def __init__(self, animations):
        Entity.__init__(self, animations)
        self.direction_id = None
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.running = False
        self.sightdist = 5
        self.max_speed = 10 # doesn't apply to player yet, but could
        self.bounce_count = 0
        #TODO: if methods/data from monster/player are universal, move them to this class.

    def updateAnimation(self, light_value = None): #
        """ updateAnimation ( int ) -> None

        Updates the animation and image of the Being based on the light that is on it. Differs from usual 
        updateImage in that we must find this being's current tile because it can change a lot.
        Currently, Beings cannot be shaded based on light value, but we could probably have them be darkened
        completely for a value of 0 if this works well for the gameplay.
        """
        if self.currenttile() == None: return
        if(light_value == None):
            light_value = self.currenttile().check_brightness()
        #IDEA: if light value is 0 at this point, set the animation either to complete darkness or to some "darkened" animation. 
        #(i.e., the bat's darkened animation appears only as two red eyes. )
        GameImage.updateAnimation(self, light_value)

    def updatePosition(self):
        """ updatePosition () -> None

        Updates the Being's position on the screen based on its current velocities.
        """
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel)

    #TODO: consider having bounce take effect here, like in player.
    def collide(self, xvel, yvel, collide_objects = None):
        """ collide (double, double, [Platform]) -> None

        Collide with all solid platforms using the collideWith method also found in Being.
        Collisions with non-platform objects are handled by other methods.
        """
        if(collide_objects == None):
            level = self.current_level
            collide_objects = level.getPlatforms()
        for c in collide_objects:
            self.collideWith(xvel, yvel, c)

    def collideWith(self, xvel, yvel, collide_object):
        """ collideWith (double, double, Platform) -> None

        If the Being is "up against" a platform (based on pygame's built-in collide method), 
        it will become flush with that platform no matter what its velocity is, and be unable 
        to move in the direction of that platform. (i.e., through the platform.)
        """
        if pygame.sprite.collide_mask(self, collide_object): #TODO: case for sloping objects
            if isinstance(collide_object, Platform) and collide_object.is_sloped:
                self.collideWithSlope(xvel, yvel, collide_object)
                return
            if xvel > 0:
                self.rect.right = collide_object.rect.left
            if xvel < 0:
                self.rect.left = collide_object.rect.right
            if yvel > 0:
                self.rect.bottom = collide_object.rect.top
                self.onGround = True
                self.yvel = 0
            if yvel < 0:
                self.rect.top = collide_object.rect.bottom

    def collideWithSlope(self, xvel, yvel, slope): #NOTE: this only works for slopes on the ground, not on the ceiling.
        if yvel == 0:
            while pygame.sprite.collide_mask(self, slope):
                self.rect.bottom -= 1
                #if xvel > 0:
                #    self.rect.right -= 1
                #if xvel < 0:
                #    self.rect.left += 1
        else:
            while pygame.sprite.collide_mask(self, slope):
                if xvel > 0:
                    self.rect.right -= 1
                if xvel < 0:
                    self.rect.left += 1
                if yvel > 0:
                    self.rect.bottom -= 1
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top += 1

    def moveTowards(self, destination):
        """ moveTowards (GameImage) -> None

        Move towards some destination, assuming the Being is not currently bouncing.
        I'm not sure I like this structure. Beings should probably just collide first,
        check bounce second, and perform whatever other actions they can only after the
        bounce check, and these should all be in single method. I'm too lazy to set that
        up right now, though.
        """
        if self.bounce_count > 0:
            self.bounce()
            return 
        distance = self.dist_from(destination)
        if(distance == 0): return
        dist_ratio = self.max_speed/distance
        self.xvel = dist_ratio*self.x_dist_from(destination, False)/32
        self.yvel = dist_ratio*self.y_dist_from(destination, False)/32

    def bounceAgainst(self, other): #this is used for a monster colliding with the player, and may be useful in other cases.
        """ bounceAgainst (Being) -> None

        Bounce against another being, starting the bounce counter so that this being cannot
        take other actions until the counter runs out.
        """
    	if(self.bounce_count > 0): return
        x_direction_sign = 1
        y_direction_sign = 1
        if(self.rect.left < other.rect.left):
            x_direction_sign = -1
        if(self.rect.top < other.rect.top):
            y_direction_sign = -1
        new_xvel = 2 * x_direction_sign
        new_yvel = 2 * y_direction_sign
        self.xvel = new_xvel
        self.yvel = new_yvel 
        self.bounce_count = 40

    def bounce(self):
        """ bounce () -> None

        Go through one iteration of "bouncing" (i.e., being knocked away from the source of the bounce)
        and reducing the bounce counter by 1.
        """
        if(self.bounce_count <= 0): 
            return
        self.collide(self.xvel,self.yvel)
        self.updatePosition()
        self.bounce_count -= 1