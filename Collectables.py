from includes import *

class Collectables:
    __metaclass__ = ABCMeta

#    def __init__(self, x, y):
#        self.x = x
#        self.y = y

    @abstractmethod
    def draw_collectable(self, x, y, animationObjs, world):
        world.surface.blit(animationObjs, (x, y))


class Coin(Collectables):
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw_collectable(self, x, y, animationObjs, world):
#        super(x, y, animationObjs, world)
        pass