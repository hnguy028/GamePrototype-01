# currently only generating coins?
from includes import *

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
