from Slot import *

# Equipment class holds information of items, and abilities currently equiped to the player
class Equipment:

    def __init__(self, width, height, slot_icon, icon_width, icon_height, slot_padding, pos=(0, 0)):

        self.width = width
        self.height = height
        self.pos = pos

        self.surface = pygame.Surface((self.width, self.height))

        self.head_gear = None
        self.chest_gear = None
        self.leg_gear = None
        self.feet_gear = None

        self.left_hand = None
        self.right_hand = None

        self.accessory1 = None
        self.accessory2 = None

        self.equipmentMatrix = []

        self.slot_icon = slot_icon
        self.icon_width = icon_width
        self.icon_height = icon_height
        self.slot_padding = slot_padding

        self.load()

    def load(self):
        self.numRows = 2
        self.numRomItems = [4, 5]

        for i in range(self.numRows):
            self.equipmentMatrix.append([])
            col_padding = (self.width - (self.numRomItems[i] * self.icon_width)) // (self.numRomItems[i] + 1)
            for j in range(self.numRomItems[i]):
                self.equipmentMatrix[i].append(Slot(self.slot_icon,
                                             i, j,
                                             self.icon_width, self.icon_height,
                                             ( (col_padding * (j+1)) + (self.icon_width * j),(self.slot_padding * (i+1)) + (self.icon_height * i))))


    def equip(self, item):
        self.head_gear = item
        self.equipmentMatrix[1][0].add(item)

    def unequip(self, x, y):
        return self.equipmentMatrix[x][y].remove()

    def draw(self, surface, pos=(-1,-1)):
        drawPos = pos
        if drawPos == (-1,-1):
            drawPos = self.pos

        # draw equipmentMatrix to inventory surface
        surface.blit(self.surface, drawPos)

        # draw background image to inventory surface
        self.surface.fill((144, 144, 144))

        # draw slots and item icons
        for list in self.equipmentMatrix:
            for slot in list:
                slot.draw(self.surface)





