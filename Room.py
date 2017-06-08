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
