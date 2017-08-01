from includes import *

# Equipment class holds information of items, and abilities currently equiped to the player
class Equipment:

    def __init__(self, width, height):
        # inventory surfaces
        self.surface = pygame.Surface((width, height))

        self.head_gear = None
        self.chest_gear = None
        self.leg_gear = None
        self.feet_gear = None

        self.left_hand = None
        self.right_hand = None

        self.accessory1 = None
        self.accessory2 = None
