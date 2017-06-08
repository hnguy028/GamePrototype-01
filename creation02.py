# Sandbox - Testing pyganim.py
from __future__ import division
import pygame
import sys
import time
import math
import pyganim
from pygame import *
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from abc import ABCMeta, abstractmethod

# Constants & Variable definition
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


# number of pixels per tile
class TileSurface:
    # size : (32) pixels
    def __init__(self, size):
        self.size = size  # Number of pixels square per tile (32)


# Window surface definition
class WindowSurface:
    # tileSize : (32)
    # roomWidth, roomHeight : size of rooms in tiles
    # worldName : string name for tmx file name
    # spawn : object from tmx containing x,y spawn location for player
    def __init__(self, tileSize, hudSize, roomWidth, roomHeight, worldName):
        # window size in pixels
        self.widthPixels = tileSize * roomWidth  # in pixels
        self.heightPixels = tileSize * roomHeight  # in pixels

        self.windowWidth = tileSize * roomWidth
        self.windowHeight = tileSize * roomHeight + tileSize * hudSize

        # create window
        self.surface = pygame.display.set_mode((self.windowWidth, self.windowHeight), 0, tileSize)
        pygame.display.set_caption('Loot 2D')

        # init map
        # helps python read as string
        assert isinstance(worldName, str)
        self.worldName = worldName
        self.gameMap = load_pygame('TileGameResources\%s.tmx' % worldName)

        # number of rooms on the current tmx defined world
        self.numRoomsX = self.gameMap.layers[0].width / roomWidth
        self.numRoomsY = self.gameMap.layers[0].height / roomHeight

        # Array holding the current map's tiles
        self.mapTiles = []

        self.playerSpawn = self.gameMap.get_object_by_name("SpawnPoint")  # defined in tmx meta

        # hudSize in tiles
        self.hudSize = hudSize

    # xRoom, yRoom : current room position in grid (1-3)
    # roomWidth, roomHeight : room size in tiles (20)
    def loadMap(self, room):
        # clear mapTiles
        del self.mapTiles[:]

        # load current tmx in the range of current frameBlocks
        for yTile in range(room.height * room.yRoom, room.height * (room.yRoom + 1)):
            for xTile in range(room.width * room.xRoom, room.width * (room.xRoom + 1)):
                tile = self.gameMap.get_tile_image(xTile, yTile, 0)
                self.mapTiles.append(tile)

    # tile size : size of tiles in pixels (32)
    # roomWidth, roomHeight : room size in tiles (20)
    def drawMap(self, tileSize, roomWidth, roomHeight):
        i = 0
        for yTile in range(roomHeight):
            for xTile in range(roomWidth):
                self.surface.blit(self.mapTiles[i], (xTile * tileSize, yTile * tileSize))
                i += 1


# Room size definition
class RoomSurface:
    # width, height : of the room in tiles (20)
    # tile : tileSurface object
    # playerSpawn : obj holding x,y location of player spawn
    def __init__(self, width, height, tileDef, playerSpawn):
        self.width = width
        self.height = height
        self.xRoom = int(playerSpawn.x // (tileDef.size * width))
        self.yRoom = int(playerSpawn.y // (tileDef.size * height))

        # init collectable booleans
        #self.collectables = Collectables()

#    def checkCollectables(self):
#        self.collectables.numCoins = 1

# TODO : draw user hud


class HUD:
    # initialize hud variables
    def __init__(self, hudSize, world):
        # hud size in tiles
        self.hudSize = hudSize

        world.surface.blit()


class Player:
    def __init__(self, world, character, health, magic, coins, direction):
        # player images
        self.front_facing = pygame.image.load('characters/%s/char_front.png' % character)
        self.back_facing = pygame.image.load('characters/%s/char_back.png' % character)
        self.right_facing = pygame.image.load('characters/%s/char_right.png' % character)
        self.left_facing = pygame.transform.flip(self.right_facing, True, False)

        # player's x,y coordinates on the current map/room
        self.x = world.playerSpawn.x % world.widthPixels
        self.y = world.playerSpawn.y % world.widthPixels
        self.direction = direction  # initial stance
        self.running = self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False

        # get sprite's pixel size
        self.width, self.height = self.front_facing.get_size()

        # player stats
        self.health = health
        self.magic = magic
        self.coins = coins

        self.walkRate = 10
        self.runRate = 1

        # creating the PygAnimation objects for walking/running in all directions
        animTypes = 'back_run back_walk front_run front_walk right_run right_walk'.split()
        self.animObjs = {}
        for animType in animTypes:
            imagesAndDurations = [('characters/%s/char_%s.%s.png' % (character, animType, str(num).rjust(3, '0')), 0.1)
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

    def move_Up(self, rate, tileSize, world, room):
        topLeft = world.gameMap.get_tile_properties(
            (self.x + (world.widthPixels * room.xRoom)) / tileSize,
            ((self.y + (world.heightPixels * room.yRoom) - rate) / tileSize),
            1)["collidable"]

        topRight = world.gameMap.get_tile_properties(
            (self.x + self.width + (world.widthPixels * room.xRoom)) / tileSize,
            ((self.y + (world.heightPixels * room.yRoom) - rate) / tileSize),
            1)["collidable"]

        if topLeft == 'false' and topRight == 'false':
            self.y -= rate

    def move_Down(self, rate, tileSize, world, room):
        bottomLeft = world.gameMap.get_tile_properties(
            (self.x + (world.widthPixels * room.xRoom)) / tileSize,
            ((self.y + rate + self.height + (world.heightPixels * room.yRoom)) / tileSize),
            1)["collidable"]

        bottomRight = world.gameMap.get_tile_properties(
            (self.x + self.width + (world.widthPixels * room.xRoom)) / tileSize,
            ((self.y + rate + self.height + (world.heightPixels * room.yRoom)) / tileSize),
            1)["collidable"]

        if bottomLeft == 'false' and bottomRight == 'false':
            self.y += rate

    def move_Left(self, rate, tileSize, world, room):
        topLeft = world.gameMap.get_tile_properties(
            (self.x - rate + (world.widthPixels * room.xRoom)) / tileSize,
            (self.y + (world.heightPixels * room.yRoom)) / tileSize,
            1)["collidable"]

        bottomLeft = world.gameMap.get_tile_properties(
            (self.x - rate + (world.widthPixels * room.xRoom)) / tileSize,
            (self.y + self.height + (world.heightPixels * room.yRoom)) / tileSize,
            1)["collidable"]

        if topLeft == 'false' and bottomLeft == 'false':
            self.x -= rate

    def move_Right(self, rate, tileSize, world, room):
        topRight = world.gameMap.get_tile_properties(
            (self.x + rate + self.width + (world.widthPixels * room.xRoom)) / tileSize,
            (self.y + (world.heightPixels * room.yRoom)) / tileSize,
            1)["collidable"]

        bottomRight = world.gameMap.get_tile_properties(
            (self.x + rate + self.width + (world.widthPixels * room.xRoom)) / tileSize,
            (self.y + self.height + (world.heightPixels * room.yRoom)) / tileSize,
            1)["collidable"]

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

    def walkRunMotion(self, world):

        # draw the correct walking/running sprite from the animation object
        self.moveConductor.play()
        # calling play() while the animation objects are already playing is okay; in that case play() is a no-op

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

    def boundsCheck(self, world, room):
        if self.x < 0:
            if room.xRoom > 0:  # load next screen in X direction
                room.xRoom -= 1
                world.loadMap(room)
                self.x = world.widthPixels - self.width  # reset character position to other side
            else:  # else stop character movement
                self.x = 0  # should never be reached
        if self.x > world.widthPixels - self.width:
            if room.xRoom < world.numRoomsX - 1:  # load next screen in X direction
                room.xRoom += 1
                world.loadMap(room)
                self.x = 0
            else:
                self.x = world.widthPixels - self.width
        if self.y < 0:
            if room.yRoom > 0:  # load next screen in Y direction
                room.yRoom -= 1
                world.loadMap(room)
                self.y = world.heightPixels - self.height
            else:
                self.y = 0
        if self.y > world.heightPixels - self.height:
            if room.yRoom < world.numRoomsY - 1:  # load next screen in Y direction
                room.yRoom += 1
                world.loadMap(room)
                self.y = 0
            else:
                self.y = world.heightPixels - self.height


class Collectables:
    __metaclass__ = ABCMeta

#    def __init__(self, x, y):
#        self.x = x
#        self.y = y

    @abstractmethod
    def draw_collectable(self, x, y, animationObjs, world):
        world.surface.blit(animationObjs, (x, y))


class Coin(Collectables):
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw_collectable(self, x, y, animationObjs, world):
#        super(x, y, animationObjs, world)
        pass


# loads map defined by the portal
def checkPortal(player, tile, room, world):
    # TODO : need to check if a portal exists in the first place (currently assuming that there is a portal on each map)
    # TODO : should work anyways, the for loop should handle null (need to test)
    portals = world.gameMap.get_layer_by_name("portals")

    for portal in portals:
        # check if player is within the bounds of the portal
        if (((player.x + (room.xRoom * world.widthPixels)) >= portal.x)
                and ((player.y + (room.yRoom * world.heightPixels)) >= portal.y)
                and ((player.x + (room.xRoom * world.widthPixels)) <= (portal.x + portal.width))
                and ((player.y + (room.yRoom * world.heightPixels)) <= (portal.y + portal.height))):

            world.gameMap = load_pygame('TileGameResources\\' + portal.worldName + '.tmx')

            world.playerSpawn = world.gameMap.get_object_by_name("SpawnPoint")

            room.xRoom = int(world.playerSpawn.x // world.widthPixels)
            room.yRoom = int(world.playerSpawn.y // world.heightPixels)

            player.x = world.playerSpawn.x % world.widthPixels
            player.y = world.playerSpawn.y % world.heightPixels

            # reload tmx of new world
            world.loadMap(room)

            # draw new world
            world.drawMap(tile.size, room.width, room.height)


# DIRTYCODE : TOBE removed
class Coin1:
    def __init__(self):
        self.coinAnimObjs = {}
        imagesAndDurations = [('collectables/coin/coin_%s.png' % (str(num).rjust(2, '0')), 0.1) for num in range(4)]
        self.coinAnimObjs['coin'] = pyganim.PygAnimation(imagesAndDurations)
        self.coinConductor = pyganim.PygConductor(self.coinAnimObjs)

        #self.x = -1
        #self.y = -1
        self.coinExists = False

    def getCoin(self, world):
        try:
            self.colLayer = world.gameMap.get_layer_by_name("collectables")
            #self.x = coinLoc.x
            #self.y = coinLoc.y
            self.coinExists = True
        except ValueError:
            self.coinExists = False

        if self.coinExists:
            self.coinConductor.play()

    def drawCoin(self, world):
        if self.coinExists:
            for coin in self.colLayer:
                if coin.name == "coin" and coin.visible:
                    self.coinAnimObjs["coin"].blit(world.surface, (coin.x, coin.y))

    def removeCoin(self, x, y):
        if self.coinExists:
            for coin in self.colLayer:
                if coin.name == "coin" and coin.visible and isNear(x, coin.x, y, coin.y, 20):
                    coin.visible = False

# TOBE removed OR implemented
def isNear(x, x2, y, y2, d):
    flag = False
    if x-d <= x2 and x+d >= x2 and y-d <= y2 and y+d >= y2:
        flag = True

    return flag
