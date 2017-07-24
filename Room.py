from constants import *

# Room size definition
class RoomSurface:
    # width, height : of the room in tiles (20)
    # playerSpawn : obj holding x,y location of player spawn
    def __init__(self, width, height, playerSpawn):
        self.width = width
        self.height = height
        self.xRoom = int(playerSpawn.x // (TILESIZE * width))
        self.yRoom = int(playerSpawn.y // (TILESIZE * height))

        # init collectable booleans
        #self.collectables = Collectables()

#    def checkCollectables(self):
#        self.collectables.numCoins = 1
