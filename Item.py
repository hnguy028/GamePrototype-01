from includes import *
from constants import *
from resource_loader import *
from Sprite import *

class Item:

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.stack = 0
        self.sprite = None

    # draw icon image in the inventory page
    def drawIcon(self, surface, pos, width, height):
        self.sprite.drawIcon(surface, pos, width, height)

    def draw(self, surface, x, y):
        self.sprite.draw(surface, (x, y))

class Weapon(Item):

    def __init__(self):
        super(Weapon, self).__init__()


#######################################################################################################################
#                                          In-game Item Definitions
#######################################################################################################################
class ItemDirectory:

    class Potions:
        small_health = "health_small"
        medium_health = "health_medium"
        large_health = "health_large"

    class Weapons:
        sword = "sword"

    class Items:
        blue_gem = "blue_gem"

# Here we define item properties and place them into a map
class ItemDictionary:

    def __init__(self):
        self.items["bronze_sword"]

    def getValue(self, itemname):
        return self.items[itemname]