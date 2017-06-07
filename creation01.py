# Sandbox - Testing pyganim.py
from __future__ import division
import pygame, sys, time, math, pyganim
from pygame import *
from pygame.locals import *
from pytmx.util_pygame import load_pygame

pygame.init()

# Constants & Variable definition

# Numbers of tiles per screen
XBLOCKSIZE = 20
YBLOCKSIZE = 20
TILESIZE = 32 # Number of pixels square per tile

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# Window Settings
WWIDTH = TILESIZE*XBLOCKSIZE
WHEIGHT = TILESIZE*YBLOCKSIZE

# Number of "screens" in x and y 
NUMBLOCKS = 3
mapGridX = 3
mapGridY = 3

# Create Window
windowSurface = pygame.display.set_mode((WWIDTH,WHEIGHT), 0, TILESIZE)
pygame.display.set_caption('Creation 01')

# load 'idle' character sprites into variables
coin0 = pygame.image.load('collectables/coin/coin_00.png')
front_facing = pygame.image.load('characters/link/char_front.png')
back_facing = pygame.image.load('characters/link/char_back.png')
right_facing = pygame.image.load('characters/link/char_right.png')
left_facing = pygame.transform.flip(right_facing, True, False)

# get sprite's pixel size
pWidth, pHeight = front_facing.get_size()

# init map to desert_world1
gameMap = load_pygame('TileGameResources\%s.tmx' % ('desert_world2'))

# creating the PygAnimation objects for walking/running in all directions
animTypes = 'back_run back_walk front_run front_walk right_run right_walk'.split()
animObjs = {}
for animType in animTypes:
    imagesAndDurations = [('characters/link/char_%s.%s.png' % (animType, str(num).rjust(3, '0')), 0.1) for num in range(6)]
    animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)

# create the right-facing sprites by copying and flipping the left-facing sprites
animObjs['left_walk'] = animObjs['right_walk'].getCopy()
animObjs['left_walk'].flip(True, False)
animObjs['left_walk'].makeTransformsPermanent()
animObjs['left_run'] = animObjs['right_run'].getCopy()
animObjs['left_run'].flip(True, False)
animObjs['left_run'].makeTransformsPermanent()

moveConductor = pyganim.PygConductor(animObjs)

#-----------------------------------------------------
coinAnimObjs = {}
imagesAndDurations = [('collectables/coin/coin_%s.png' % (str(num).rjust(2, '0')), 0.1) for num in range(4)]
coinAnimObjs['coin'] = pyganim.PygAnimation(imagesAndDurations)
coinConductor = pyganim.PygConductor(coinAnimObjs)
coinx = -1
coiny = -1
coinq = False

def getCoin():
    coinx = 0;
    coiny = 0;
    # creating the PygAnimation objects for coin
    #coinAnimTypes = '00 01 02 03'.split()
    try:
        coinLoc = gameMap.get_object_by_name("coin1") # defined in tmx meta
        coinx = coinLoc.x % WWIDTH
        coiny = coinLoc.y % WHEIGHT
        coinq = True
    except ValueError:
        coinq = False

    if coinq:
        coinConductor.play()
        
    return coinx,coiny,coinq
#-----------------------------------------------------

direction = DOWN # initial stance

# clock cycle
mainClock = pygame.time.Clock()

# classes and objects to be added
#class Player:

#    def __init__(self, x, y, height, width, health, magic, coins):
#        self.x = x
#        self.y = y
#        self.height = height
#        self.width = width
#        self. health = health
#        self.magic = magic
#        self.coins = coins


# Movement Speed
WALKRATE = 10
RUNRATE = 1

running = moveUp = moveDown = moveLeft = moveRight = False

# Character's x, y spawn coordinates
spawn = gameMap.get_object_by_name("SpawnPoint") # defined in tmx meta

# Defines the game frame currently displayed
frameBlockX = int(spawn.x // WWIDTH) + 1
frameBlockY = int(spawn.y // WHEIGHT) + 1

x = spawn.x % WWIDTH
y = spawn.y % WHEIGHT

# Array holding the current map's tiles
mapTiles = []

# loop to add tiles within the current frame to mapTiles

def loadMap(xRoom, yRoom, roomWidth, roomHeight):
    #clear mapTiles
    del mapTiles[:]

    # load current tmx in the range of current frameBlocks
    for yTile in range(roomHeight*(yRoom),roomHeight*(yRoom+1)):
        for xTile in range(roomWidth*(xRoom),roomWidth*(xRoom+1)):
            tile = gameMap.get_tile_image(xTile,yTile,0)
            mapTiles.append(tile)
    print gameMap.layers[0].width

def drawMap(tileSize, roomWidth, roomHeight):
    i=0
    for yTile in range(roomHeight):
        for xTile in range(roomWidth):
            windowSurface.blit(mapTiles[i],(xTile*tileSize,yTile*tileSize))
            i+= 1

loadMap(frameBlockX-1, frameBlockY-1, XBLOCKSIZE,YBLOCKSIZE)


# Game loop
while True:
    #display tiles defined in mapTiles
    drawMap(32,XBLOCKSIZE,YBLOCKSIZE)

    #-------------------------------------
    # draw coin if it exists
    if coinq == True:
        coinAnimObjs['coin'].blit(windowSurface, (coinx, coiny))

    #-------------------------------------

    for event in pygame.event.get(): # event handling loop

        # handle exit button press
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            # if shift key is pressed init player running
            if event.key in (K_LSHIFT, K_RSHIFT):
                running = True

            if event.key == K_UP:
                moveUp = True;
                moveDown = False;
                if not moveLeft and not moveRight:
                    # only change the direction to up if the player wasn't moving left/right
                    direction = UP
            elif event.key == K_DOWN:
                moveDown = True
                moveUp = False
                if not moveLeft and not moveRight:
                    direction = DOWN
            elif event.key == K_LEFT:
                moveLeft = True
                moveRight = False
                if not moveUp and not moveDown:
                    direction = LEFT
            elif event.key == K_RIGHT:
                moveRight = True
                moveLeft = False
                if not moveUp and not moveDown:
                    direction = RIGHT

        elif event.type == KEYUP:
            if event.key in (K_LSHIFT, K_RSHIFT):
                # player has stopped running
                running = False

            if event.key == K_UP:
                moveUp = False
                # if the player was moving in a sideways direction before, change the direction the player is facing.
                if moveLeft:
                    direction = LEFT
                if moveRight:
                    direction = RIGHT
            elif event.key == K_DOWN:
                moveDown = False
                if moveLeft:
                    direction = LEFT
                if moveRight:
                    direction = RIGHT
            elif event.key == K_LEFT:
                moveLeft = False
                if moveUp:
                    direction = UP
                if moveDown:
                    direction = DOWN
            elif event.key == K_RIGHT:
                moveRight = False
                if moveUp:
                    direction = UP
                if moveDown:
                    direction = DOWN

    if moveUp or moveDown or moveLeft or moveRight:
        # draw the correct walking/running sprite from the animation object
        moveConductor.play() # calling play() while the animation objects are already playing is okay; in that case play() is a no-op
        if running:
            if direction == UP:
                animObjs['back_run'].blit(windowSurface, (x, y))
            elif direction == DOWN:
                animObjs['front_run'].blit(windowSurface, (x, y))
            elif direction == LEFT:
                animObjs['left_run'].blit(windowSurface, (x, y))
            elif direction == RIGHT:
                animObjs['right_run'].blit(windowSurface, (x, y))
        else:
            # walking
            if direction == UP:
                animObjs['back_walk'].blit(windowSurface, (x, y))
            elif direction == DOWN:
                animObjs['front_walk'].blit(windowSurface, (x, y))
            elif direction == LEFT:
                animObjs['left_walk'].blit(windowSurface, (x, y))
            elif direction == RIGHT:
                animObjs['right_walk'].blit(windowSurface, (x, y))

        #DEBUG
        #print "x: ",(x+(32*20*(frameBlockX-1)))/32,", y: ",(y+(32*20*(frameBlockY-1)))/32

        if running:
            rate = RUNRATE
        else:
            rate = WALKRATE

        if moveUp:
            topLeft = gameMap.get_tile_properties( ( x + (WWIDTH*(frameBlockX-1)) ) / TILESIZE, math.floor(( y + (WHEIGHT*(frameBlockY-1)) - rate) / TILESIZE), 1)["collidable"]
            topRight = gameMap.get_tile_properties( ( x + pWidth + (WWIDTH*(frameBlockX-1)) ) / TILESIZE, (( y + (WHEIGHT*(frameBlockY-1)) - rate) / TILESIZE), 1)["collidable"]
            if (topLeft == 'false' and topRight == 'false'):
                y -= rate
        if moveDown:
            bottomLeft = gameMap.get_tile_properties( ( x + (WWIDTH*(frameBlockX-1)) ) / TILESIZE, math.floor( ( y + rate + pHeight + (WHEIGHT*(frameBlockY-1)) ) / TILESIZE), 1)["collidable"]
            bottomRight = gameMap.get_tile_properties(math.floor( x + pWidth + (WWIDTH*(frameBlockX-1)) ) / TILESIZE, math.floor( ( y + rate + pHeight + (WHEIGHT*(frameBlockY-1)) ) / TILESIZE), 1)["collidable"]
            if (bottomLeft == 'false' and bottomRight == 'false'):
                y += rate
        if moveLeft:
            topLeft = gameMap.get_tile_properties( ( x - rate + (WWIDTH*(frameBlockX-1))) / TILESIZE, ( y + (WHEIGHT*(frameBlockY-1)) ) / TILESIZE, 1)["collidable"]
            bottomLeft = gameMap.get_tile_properties( ( x - rate + (WWIDTH*(frameBlockX-1)) ) / TILESIZE, ( y + pHeight + (WHEIGHT*(frameBlockY-1)) ) / TILESIZE, 1)["collidable"]
            if (topLeft == 'false' and bottomLeft == 'false'):
                x -= rate
        if moveRight:
            topRight = gameMap.get_tile_properties( ( x + rate + pWidth + (WWIDTH*(frameBlockX-1)) ) / TILESIZE, ( y + (WHEIGHT*(frameBlockY-1)) ) / TILESIZE, 1)["collidable"]
            bottomRight = gameMap.get_tile_properties( ( x + rate + pWidth + (WWIDTH*(frameBlockX-1))) / TILESIZE, ( y + pHeight + (WHEIGHT*(frameBlockY-1)) ) / TILESIZE, 1)["collidable"]
            if (topRight == 'false' and bottomRight == 'false'):
                x += rate

    else:
        # standing still
        moveConductor.stop() # calling stop() while the animation objects are already stopped is okay; in that case stop() is a no-op
        if direction == UP:
            windowSurface.blit(back_facing, (x, y))
        elif direction == DOWN:
            windowSurface.blit(front_facing, (x, y))
        elif direction == LEFT:
            windowSurface.blit(left_facing, (x, y))
        elif direction == RIGHT:
            windowSurface.blit(right_facing, (x, y))

    # make sure the player does move off the screen
    if x < 0:
        if frameBlockX > 1:  # load next screen in X direction
            frameBlockX -= 1
            loadMap(frameBlockX-1, frameBlockY-1, XBLOCKSIZE,YBLOCKSIZE)
            x = WWIDTH - pWidth # reset character position to other side
        else: # else stop character movement
            x = 0 # should never be reached
    if x > WWIDTH - pWidth:
        if frameBlockX < mapGridX: # load next screen in X direction
            frameBlockX += 1
            loadMap(frameBlockX-1, frameBlockY-1, XBLOCKSIZE,YBLOCKSIZE)
            x = 0
        else:
            x = WWIDTH - pWidth
    if y < 0:
        if frameBlockY > 1: # load next screen in Y direction
            frameBlockY -= 1
            loadMap(frameBlockX-1, frameBlockY-1, XBLOCKSIZE,YBLOCKSIZE)
            y = WHEIGHT - pHeight
        else:
            y = 0
    if y > WHEIGHT - pHeight:
        if frameBlockY < mapGridY: # load next screen in Y direction
            frameBlockY += 1
            loadMap(frameBlockX-1, frameBlockY-1, XBLOCKSIZE,YBLOCKSIZE)
            y = 0
        else:
            y = WHEIGHT - pHeight

    # load alternate map defined by the portal object
    portal = gameMap.get_object_by_name("Portal")

    # check if player is within the bounds of the portal
    if ( ( (x + ( (frameBlockX-1)*WWIDTH) )  >= (portal.x) )
         and ( (y + ( (frameBlockY-1)*WHEIGHT) ) >= (portal.y) )
         and ( (x + ( (frameBlockX-1)*WWIDTH) ) <= (portal.x + portal.width) )
         and ( (y + ( (frameBlockY-1)*WHEIGHT) ) <= (portal.y + portal.height) ) ):

        gameMap = load_pygame('TileGameResources\\'+portal.worldName+'.tmx')

        spawn = gameMap.get_object_by_name("SpawnPoint") # defined in tmx meta
            
        frameBlockX = int(spawn.x // WWIDTH) + 1
        frameBlockY = int(spawn.y // WHEIGHT) + 1

        x = spawn.x % WWIDTH
        y = spawn.y % WHEIGHT

        coinx,coiny,coinq = getCoin()
        loadMap(frameBlockX-1, frameBlockY-1, XBLOCKSIZE,YBLOCKSIZE)

    #windowSurface.blit(instructionSurf, instructionRect)

    pygame.display.update()
    mainClock.tick(30) # Feel free to experiment with any FPS setting.
