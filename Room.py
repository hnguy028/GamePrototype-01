from Mob import *
from resource_loader import *

# Room size definition
class RoomSurface:
    # width, height : of the room in tiles (20)
    # playerSpawn : obj holding x,y location of player spawn
    def __init__(self, worldName, pos=(0, 0)):
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

        self.playerSpawn = self.gameMap.get_object_by_name("init_spawn_point")  # defined in tmx meta

        self.xRoom = int(self.playerSpawn.x // (TILESIZE * self.tileWidth))
        self.yRoom = int(self.playerSpawn.y // (TILESIZE * self.tileHeight))

        self.surface = pygame.Surface((self.pixelWidth, self.pixelHeight))
        self.pos = pos

        # dictionary of layers to be drawn
        self.tileLayers = {}

        # array to hold the tiles of the current map
        for i in range(tmxCodes.DRAWN_LAYERS):
            self.tileLayers[str(i)] = []

        # layer -> object_list, dictionary
        self.objects = {}
        for layer_name in tmxCodes.OBJECT_LAYERS:
            self.objects[layer_name] = []

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

                self.numRoomsX = self.gameMap.layers[0].width / self.tileWidth
                self.numRoomsY = self.gameMap.layers[0].height / self.tileHeight

        # load in enemies layer, and collectables layer

    # tile size : size of tiles in pixels (32)
    # roomWidth, roomHeight : room size in tiles (20)
    def drawMap(self, surface):
        surface.blit(self.surface, self.pos)

        # loop through layers to be drawn
        for layer in range(tmxCodes.DRAWN_LAYERS):
            i = 0

            # loop through the 2D grid of tiles
            for yTile in range(ROOMHEIGHT):
                for xTile in range(ROOMWIDTH):
                    # draw the tile
                    self.surface.blit(self.tileLayers[str(layer)][i], (xTile * TILESIZE, yTile * TILESIZE))
                    i += 1

    def changeMap(self, new_world_name):
        prev_world_name = self.worldName

        self.worldName = new_world_name

        # load tmx map file
        self.gameMap = load_pygame(MAPS_DIRECTORY + '%s.tmx' % self.worldName)

        spawns = {}

        try:
            # load all spawn points (worldName -> spawnLocation)
            for spawn in self.gameMap.get_layer_by_name(tmxCodes.SPAWN_LAYER):
                spawns[spawn.worldName] = spawn

            # set the spawn point to the previous world's portal destination
            self.playerSpawn = spawns[prev_world_name]
        except ValueError:
            # if layer only has one object
            self.playerSpawn = self.gameMap.get_object_by_name(tmxCodes.SPAWN_POINT_CODE)

        # recalculate the room frame from spawn
        self.xRoom = int(self.playerSpawn.x / self.pixelWidth)
        self.yRoom = int(self.playerSpawn.y / self.pixelHeight)

        # reload tmx of new world
        self.loadMap()

        # load world_name into gameMap
        self.load_objects()

    # load in positions of npcs and collectables of the current map
    def load_objects(self):
        # loop through object layers
        for layer_name in tmxCodes.OBJECT_LAYERS:
            try:
                # grab the object layer
                layer = self.gameMap.get_layer_by_name(layer_name)
            except ValueError:
                # if it doesnt exist then skip
                continue

            # iterate through the objects in the layer
            for obj in layer:
                # add object to list, at layer_name key
                self.objects[layer_name].append(obj)


    # return the surface of the tile at (x, y) of the collision/meta layer
    def get_tile(self, x, y):
        # TODO : if x, y are out of the tmx bounds, will throw value error
        return self.gameMap.get_tile_image(int(x + (self.xRoom * self.tileWidth)), int(y + (self.yRoom * self.tileHeight)), tmxCodes.META_LAYER)