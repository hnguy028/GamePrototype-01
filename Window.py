from constants import *
from includes import *


# Window surface definition
class WindowSurface:
    # tileSize : in pixels
    # hudSize in pixels
    # roomWidth, roomHeight : size of rooms in tiles
    # worldName : string name for tmx file name
    # spawn : object from tmx containing x,y spawn location for player
    def __init__(self, hudSize, roomWidth, roomHeight, worldName):
        self.surfaceWidth = TILESIZE * roomWidth
        self.surfaceHeight = TILESIZE * roomHeight + hudSize

        # create window
        self.surface = pygame.display.set_mode((self.surfaceWidth, self.surfaceHeight), 0, TILESIZE)
        pygame.display.set_caption(GAME_TITLE)
        pygame.display.set_icon(pygame.image.load(GAME_ICON))