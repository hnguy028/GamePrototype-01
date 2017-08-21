from includes import *
from resource_loader import *
from Controls import *

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

        # list of points relative to the player, used to check for collision
        self.handler_points = []

        self.direction = direction  # initial stance
        self.running = self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False

        # get sprite's pixel size
        self.width, self.height = self.front_facing.get_size()

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

        # TODO : might need to move conductor to the game loop
        self.moveConductor = pyganim.PygConductor(self.animObjs)
        self.attackConductor = None

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
        topLeft = room.gameMap.get_tile_properties(
            (self.x + (room.pixelWidth * room.xRoom)) / tileSize,
            ((self.y + (room.pixelHeight * room.yRoom) - rate) / tileSize),
            tmxCodes.META_LAYER)[tmxCodes.IMPASSIVE_CODE]

        topRight = room.gameMap.get_tile_properties(
            (self.x + self.width + (room.pixelWidth * room.xRoom)) / tileSize,
            ((self.y + (room.pixelHeight * room.yRoom) - rate) / tileSize),
            tmxCodes.META_LAYER)[tmxCodes.IMPASSIVE_CODE]

        if topLeft == 'false' and topRight == 'false':
            self.y -= rate

    def move_Down(self, rate, tileSize, room):
        bottomLeft = room.gameMap.get_tile_properties(
            (self.x + (room.pixelWidth * room.xRoom)) / tileSize,
            ((self.y + rate + self.height + (room.pixelHeight * room.yRoom)) / tileSize),
            tmxCodes.META_LAYER)[tmxCodes.IMPASSIVE_CODE]

        bottomRight = room.gameMap.get_tile_properties(
            (self.x + self.width + (room.pixelWidth * room.xRoom)) / tileSize,
            ((self.y + rate + self.height + (room.pixelHeight * room.yRoom)) / tileSize),
            tmxCodes.META_LAYER)[tmxCodes.IMPASSIVE_CODE]

        if bottomLeft == 'false' and bottomRight == 'false':
            self.y += rate

    def move_Left(self, rate, tileSize, room):
        topLeft = room.gameMap.get_tile_properties(
            (self.x - rate + (room.pixelWidth * room.xRoom)) / tileSize,
            (self.y + (room.pixelHeight * room.yRoom)) / tileSize,
            tmxCodes.META_LAYER)[tmxCodes.IMPASSIVE_CODE]

        bottomLeft = room.gameMap.get_tile_properties(
            (self.x - rate + (room.pixelWidth * room.xRoom)) / tileSize,
            (self.y + self.height + (room.pixelHeight * room.yRoom)) / tileSize,
            tmxCodes.META_LAYER)[tmxCodes.IMPASSIVE_CODE]

        if topLeft == 'false' and bottomLeft == 'false':
            self.x -= rate

    def move_Right(self, rate, tileSize, room):
        topRight = room.gameMap.get_tile_properties(
            (self.x + rate + self.width + (room.pixelWidth * room.xRoom)) / tileSize,
            (self.y + (room.pixelHeight * room.yRoom)) / tileSize,
            tmxCodes.META_LAYER)[tmxCodes.IMPASSIVE_CODE]

        bottomRight = room.gameMap.get_tile_properties(
            (self.x + rate + self.width + (room.pixelWidth * room.xRoom)) / tileSize,
            (self.y + self.height + (room.pixelHeight * room.yRoom)) / tileSize,
            tmxCodes.META_LAYER)[tmxCodes.IMPASSIVE_CODE]

        if topRight == 'false' and bottomRight == 'false':
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

    # check collision with the given x,y coordinates
    def collision_check(self, x=0, y=0):
        for point in self.handler_points:
            if self.point_collision_check(point.x + x, point.y + y):
                # return the object collided with
                pass
        return None

    # check if the given point collides with another entity
    def point_collision_check(self, x, y):
        pass

class _Point:
    def __init__(self, p):
        self.x = p[0]
        self.y = p[1]
