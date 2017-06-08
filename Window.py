from includes import *

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
