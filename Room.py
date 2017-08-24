from resource_loader import *

# Room size definition
class RoomSurface:
    # width, height : of the room in tiles (20)
    # playerSpawn : obj holding x,y location of player spawn
    def __init__(self, worldName):
        self.tileWidth = ROOMWIDTH
        self.tileHeight = ROOMHEIGHT

        # calculate room size in pixels
        self.pixelWidth = TILESIZE * ROOMWIDTH
        self.pixelHeight = TILESIZE * ROOMHEIGHT

        # init map
        self.worldName = worldName
        self.gameMap = load_pygame(MAPS_DIRECTORY + '%s.tmx' % worldName)

        # number of rooms on the current tmx defined world
        self.numRoomsX = self.gameMap.layers[0].width / self.tileWidth
        self.numRoomsY = self.gameMap.layers[0].height / self.tileHeight

        self.playerSpawn = self.gameMap.get_object_by_name(tmxCodes.SPAWN_CODE)  # defined in tmx meta

        self.xRoom = int(self.playerSpawn.x // (TILESIZE * self.tileWidth))
        self.yRoom = int(self.playerSpawn.y // (TILESIZE * self.tileHeight))

        # dictionary of layers to be drawn
        self.tileLayers = {}

        # array to hold the tiles of the current map
        for i in range(tmxCodes.DRAWN_LAYERS):
            self.tileLayers[str(i)] = []

    # xRoom, yRoom : current room position in grid (1-3)
    # roomWidth, roomHeight : room size in tiles (20)
    def loadMap(self):
        # clear mapTiles
        for layer in range(tmxCodes.DRAWN_LAYERS):
            del self.tileLayers[str(layer)][:]
            self.tileLayers[str(layer)] = []

        for layer in range(tmxCodes.DRAWN_LAYERS):
            # load current tmx in the range of current frameBlocks
            for yTile in range(self.tileHeight * self.yRoom, self.tileHeight * (self.yRoom + 1)):
                for xTile in range(self.tileWidth * self.xRoom, self.tileWidth * (self.xRoom + 1)):
                    self.tileLayers[str(layer)].append(self.gameMap.get_tile_image(xTile, yTile, layer))

    # tile size : size of tiles in pixels (32)
    # roomWidth, roomHeight : room size in tiles (20)
    def drawMap(self, surface):
        for layer in range(tmxCodes.DRAWN_LAYERS):
            i = 0
            for yTile in range(ROOMHEIGHT):
                for xTile in range(ROOMWIDTH):
                    surface.blit(self.tileLayers[str(layer)][i], (xTile * TILESIZE, yTile * TILESIZE))
                    i += 1

    # return the surface of the tile at (x, y) of the collision/meta layer
    def get_tile(self, x, y):
        return self.gameMap.get_tile_image(x + (self.xRoom * self.tileWidth), y + (self.yRoom * self.tileHeight), tmxCodes.META_LAYER)



# init collectable booleans
# self.collectables = Collectables()

# def checkCollectables(self):
#        self.collectables.numCoins = 1
