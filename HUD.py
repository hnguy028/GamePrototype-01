from Loot_2D import *
from constants import *
from pyganim import *

class HUD:
    # initialize hud variables
    def __init__(self):
        self.test = None

        # window

    def initHUD(self):
        print("Init HUD")

    # draws the HUD to window
    # x,y  : top left corner from which to draw the HUD
    # height, width : size in # of tiles, to draw the hud
    def drawHUD(self, x, y, height, width):
        i = 0
        for yTile in range(height):
            for xTile in range(width):
                self.surface.blit(self.mapTiles[i], (xTile * TILESIZE, yTile * TILESIZE))
                i += 1

    def drawRect(self, surface):
        pygame.draw.rect(surface, (230, 50, 50),
                         Rect((0, TILESIZE * ROOMHEIGHT), (TILESIZE * ROOMWIDTH, TILESIZE * HUDSIZE_BOTTOM)))
