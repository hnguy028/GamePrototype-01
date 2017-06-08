class HUD:
    # initialize hud variables
    def __init__(self, topSize, bottomSize, window):
        # hud size in tiles
        self.topSize = topSize
        self.bottomSize = bottomSize

        # window

    def initHUD(self):
        print("Init HUD")

    # draws the HUD to window
    # x,y  : top left corner from which to draw the HUD
    # height, width : size in # of tiles, to draw the hud
    def drawHUD(self, x, y, height, width, tile):
        i = 0
        for yTile in range(height):
            for xTile in range(width):
                self.surface.blit(self.mapTiles[i], (xTile * tile.size, yTile * tile.size))
                i += 1
