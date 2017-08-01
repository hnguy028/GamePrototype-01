from resource_loader import *
from Sprite import *

class Item:

    def __init__(self, name, spritefile, type, width=-1, height=-1):
        self.name = name
        self.type = type
        self.spritefile = spritefile
        self.sprite = Sprite(imageLibrary.load(self.spritefile, width, height))

    # draw icon image in the inventory page
    def draw(self, surface, width, height, pos):
        self.sprite.drawIcon(surface, width, height, pos)

class Weapon(Item):

    def __init__(self):
        super(Weapon, self).__init__()


#######################################################################################################################
#                                          Item Definitions
#######################################################################################################################
class ItemDirectory:

    class Potions:
        small_health = "health_small"
        medium_health = "health_medium"
        large_health = "health_large"

    class Weapons:
        sword = "sword"

class ItemTypes:
    potion = "potion"

class CurrencyTypes:
    None

# Here we define item properties and place them into a map
class ItemDictionary:

    def __init__(self):
        self.items["bronze_sword"]

    def getValue(self, itemname):
        return self.items[itemname]