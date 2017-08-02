from Slot import *

# Equipment class holds information of items, and abilities currently equiped to the player
class Equipment:

    def __init__(self, width, height, slot_icon, icon_width, icon_height, slot_padding, pos=(0, 0)):

        self.width = width
        self.height = height
        self.pos = pos

        self.surface = pygame.Surface((self.width, self.height))

        self.equipmentKeys = ["left_hand", "accessory1", "accessory2", "right_hand", "head_gear", "chest_gear", "waist_gear", "leg_gear", "feet_gear"]
        self.equipmentMap = {}
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

    def move(self, x, y, left, down):
        # TODO : this function does not necessarily switch cells when difference in size > 2
        res_x = min(len(self.equipmentMatrix[y]) - 1, x + left) if left > 0 else max(0, x + left)
        res_y = y

        if not down == 0:
            res_y = min(max(0, y + down), len(self.equipmentMatrix) - 1)
            res_x = min(len(self.equipmentMatrix[res_y]) - 1, max(0, res_x))

        return res_x, res_y
