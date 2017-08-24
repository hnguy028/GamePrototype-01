from resource_loader import *
from Controls import *
import math

class Player:
    def __init__(self, room, inventory, spawn, character, health, magic, direction):
        # player images
        self.front_facing = pygame.image.load(CHARACTER_DIRECTORY + '%s/char_front.png' % character)
        self.back_facing = pygame.image.load(CHARACTER_DIRECTORY + '%s/char_back.png' % character)
        self.right_facing = pygame.image.load(CHARACTER_DIRECTORY + '%s/char_right.png' % character)
        self.left_facing = pygame.transform.flip(self.right_facing, True, False)

        # player's x,y coordinates on the current map/room
        self.x = spawn.x % room.pixelWidth
        self.y = spawn.y % room.pixelHeight

        self.direction = direction  # initial stance
        self.running = self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False

        # get sprite's pixel size
        self.width, self.height = self.front_facing.get_size()
        print(str(self.width) + str(self.height))

        # player stats
        self.health = health
        self.magic = magic
        self.experience = 0

        self.inventory = inventory

        self.walkRate = CHAR_WALKRATE
        self.runRate = CHAR_RUNRATE

        # creating the PygAnimation objects for walking/running in all directions
        animTypes = 'back_run back_walk front_run front_walk right_run right_walk'.split()
        self.animObjs = {}
        for animType in animTypes:
            imagesAndDurations = [(CHARACTER_DIRECTORY + '%s/char_%s.%s.png' % (character, animType, str(num).rjust(3, '0')), 0.1)
                                  for num in range(6)]
            self.animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)

        # create the right-facing sprites by copying and flipping the left-facing sprites
        self.animObjs['left_walk'] = self.animObjs['right_walk'].getCopy()
        self.animObjs['left_walk'].flip(True, False)
        self.animObjs['left_walk'].makeTransformsPermanent()
        self.animObjs['left_run'] = self.animObjs['right_run'].getCopy()
        self.animObjs['left_run'].flip(True, False)
        self.animObjs['left_run'].makeTransformsPermanent()

        self.moveConductor = pyganim.PygConductor(self.animObjs)
        self.attackConductor = None

        # list of points relative to the player, used to check for collision (offsets)
        self.handler_points = [
            _Point((0, 0)),
            _Point((0, self.height)),
            _Point((self.width, 0)),
            _Point((self.width, self.height))
        ]

    # handles if key has been pushed down, taking a reference to event
    def handleKeyDown(self, e):
        # if shift key is pressed init player running
        if e.key in (K_LSHIFT, K_RSHIFT):
            self.running = True

        if e.key == K_UP:
            self.moveUp = True
            self.moveDown = False
            if not self.moveLeft and not self.moveRight:
                # only change the direction to up if the player wasn't moving left/right
                self.direction = UP
        elif e.key == K_DOWN:
            self.moveDown = True
            self.moveUp = False
            if not self.moveLeft and not self.moveRight:
                self.direction = DOWN
        elif e.key == K_LEFT:
            self.moveLeft = True
            self.moveRight = False
            if not self.moveUp and not self.moveDown:
                self.direction = LEFT
        elif e.key == K_RIGHT:
            self.moveRight = True
            self.moveLeft = False
            if not self.moveUp and not self.moveDown:
                self.direction = RIGHT
        elif e.key == C_ATTACK:
            if not self.attackConductor:
                self.attack(None)
            else:
                self.stopAttack()

    def handleKeyUp(self, e):
        if e.key in (K_LSHIFT, K_RSHIFT):
            # player has stopped running
            self.running = False

        if e.key == K_UP:
            self.moveUp = False
            # if the player was moving in a sideways direction before, change the direction the player is facing.
            if self.moveLeft:
                self.direction = LEFT
            if self.moveRight:
                self.direction = RIGHT
        elif e.key == K_DOWN:
            self.moveDown = False
            if self.moveLeft:
                self.direction = LEFT
            if self.moveRight:
                self.direction = RIGHT
        elif e.key == K_LEFT:
            self.moveLeft = False
            if self.moveUp:
                self.direction = UP
            if self.moveDown:
                self.direction = DOWN
        elif e.key == K_RIGHT:
            self.moveRight = False
            if self.moveUp:
                self.direction = UP
            if self.moveDown:
                self.direction = DOWN
        elif e.key == K_l:
            self.check_collide()

    def check_collide(self, rate, room):
        #pytmx.TiledObjectGroup.
        return room.gameMap.get_tile_properties(
            (self.x + rate + self.width + (room.pixelWidth * room.xRoom)) / TILESIZE,
            (self.y + (room.pixelHeight * room.yRoom)) / TILESIZE,
            tmxCodes.STRUCTURES_LAYER)

    def move_Up(self, rate, tileSize, room):

        meta_code = self.get_meta(room, self.x, self.y - rate)

        if not meta_code == tmxCodes.META_CODE_FREE:
            # if collides with something, stop
            return

        self.y -= rate

    def move_Down(self, rate, tileSize, room):

        meta_code = self.get_meta(room, self.x, self.y + rate)

        if not meta_code == tmxCodes.META_CODE_FREE:
            # if collides with something, stop
            return

        self.y += rate

    def move_Left(self, rate, tileSize, room):
        meta_code = self.get_meta(room, self.x - rate, self.y)

        if not meta_code == tmxCodes.META_CODE_FREE:
            # if collides with something, stop
            return

        self.x -= rate

    def move_Right(self, rate, tileSize, room):
        meta_code = self.get_meta(room, self.x + rate, self.y)

        if not meta_code == tmxCodes.META_CODE_FREE:
            # if collides with something, stop
            return

        self.x += rate

    def idle(self, world):
        # standing still
        self.moveConductor.stop()
        # calling stop() while the animation objects are already stopped is okay; in that case stop() is a no-op

        if self.direction == UP:
            world.surface.blit(self.back_facing, (self.x, self.y))
        elif self.direction == DOWN:
            world.surface.blit(self.front_facing, (self.x, self.y))
        elif self.direction == LEFT:
            world.surface.blit(self.left_facing, (self.x, self.y))
        elif self.direction == RIGHT:
            world.surface.blit(self.right_facing, (self.x, self.y))

        if self.attackConductor:
            self.attackConductor.blit(world.surface, (self.x+10, self.y-50))


    def walkRunMotion(self, world):

        # draw the correct walking/running sprite from the animation object
        self.moveConductor.play()
        # calling play() while the animation objects are already playing is okay; in that case play() is a no-op

        # TODO : change 'back_run', 'front_run' ... to global variables / make more dynamic

        if self.running:
            if self.direction == UP:
                self.animObjs['back_run'].blit(world.surface, (self.x, self.y))
            elif self.direction == DOWN:
                self.animObjs['front_run'].blit(world.surface, (self.x, self.y))
            elif self.direction == LEFT:
                self.animObjs['left_run'].blit(world.surface, (self.x, self.y))
            elif self.direction == RIGHT:
                self.animObjs['right_run'].blit(world.surface, (self.x, self.y))
        else:
            # walking
            if self.direction == UP:
                self.animObjs['back_walk'].blit(world.surface, (self.x, self.y))
            elif self.direction == DOWN:
                self.animObjs['front_walk'].blit(world.surface, (self.x, self.y))
            elif self.direction == LEFT:
                self.animObjs['left_walk'].blit(world.surface, (self.x, self.y))
            elif self.direction == RIGHT:
                self.animObjs['right_walk'].blit(world.surface, (self.x, self.y))

    def attack(self, world, attack=None):
        if attack == None:
            self.attackConductor = animationLibrary.boltAnim

        self.attackConductor.play()
        # find player center
        # attack radius/distance from player
        # attack direction
        # collision detection with any object within radius
        pass

    def stopAttack(self):
        self.attackConductor.stop()
        self.attackConductor = None

    # check if player has move beyond the frame
    def boundsCheck(self, room):
        if self.x < 0:
            if room.xRoom > 0:  # load next screen in X direction
                room.xRoom -= 1
                room.loadMap()
                self.x = room.pixelWidth - self.width  # reset character position to other side
            else:  # else stop character movement
                self.x = 0  # should never be reached
        if self.x > room.pixelWidth - self.width:
            if room.xRoom < room.numRoomsX - 1:  # load next screen in X direction
                room.xRoom += 1
                room.loadMap()
                self.x = 0
            else:
                self.x = room.pixelWidth - self.width
        if self.y < 0:
            if room.yRoom > 0:  # load next screen in Y direction
                room.yRoom -= 1
                room.loadMap()
                self.y = room.pixelHeight - self.height
            else:
                self.y = 0
        if self.y > room.pixelHeight - self.height:
            if room.yRoom < room.numRoomsY - 1:  # load next screen in Y direction
                room.yRoom += 1
                room.loadMap()
                self.y = 0
            else:
                self.y = room.pixelHeight - self.height

    def apply_item(self, item):
        if item.type == "potion":
            self.health = max(100,10)

    # returns the meta code at the given x,y coordinates
    def get_meta(self, room, x=0, y=0):

        for point in self.handler_points:

            rgb = self.get_meta_rgb(room, point.x + x, point.y + y)

            if _rgb_sim(rgb, tmxCodes.META_RGB_FREE):
                return tmxCodes.META_CODE_FREE

            elif _rgb_sim(rgb, tmxCodes.META_RGB_BLOCK):
                return tmxCodes.META_CODE_BLOCK

        return None

    def get_meta_rgb(self, room, x, y):
        # need to calculate the number of pixels into the tile
        p_x, p_y = int(x % TILESIZE), int(y % TILESIZE)

        # get tiles represented by the coordinates
        tile = room.get_tile(math.floor(x / TILESIZE), math.floor(y / TILESIZE))

        # temp surface
        surface = pygame.Surface((32, 32))
        surface.fill((255, 255, 255))

        # place tile on surface
        surface.blit(tile, (0, 0))

        # return rgba value at coordinates
        return surface.get_at((p_x, p_y))

# return true of the similarity between 2 rbg values are less than the cos difference
def _rgb_sim(self, other, cos=2):
    return (abs(self[0] - other[0]) < cos) and (abs(self[1] - other[1]) < cos) and (abs(self[2] - other[2]) < cos)

class _Point:
    def __init__(self, p):
        self.x = p[0]
        self.y = p[1]
