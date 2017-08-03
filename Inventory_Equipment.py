from Slot import *

# Equipment class holds information of items, and abilities currently equiped to the player
class InventoryEquipment:

    def __init__(self, width, height, slot_icon, icon_width, icon_height, slot_padding, pos=(0, 0)):

        self.width = width
        self.height = height
        self.pos = pos

        self.surface = pygame.Surface((self.width, self.height))

        self.equipmentKeys = ["left_hand", "accessory1", "ammunition", "accessory2", "right_hand", "head_gear", "chest_gear", "waist_gear", "leg_gear", "feet_gear"]

        self.equipmentMap = {}
        self.equipmentMatrix = []

        self.slot_icon = slot_icon
        self.icon_width = icon_width
        self.icon_height = icon_height
        self.slot_padding = slot_padding

        self.numRows = 2
        self.numRomItems = [5, 5]

        self.cursor_x = 0
        self.cursor_y = 0
        self.hoverSlot = None
        self.selectedSlot = None

        self.isFocused = False

        self.load()

    # load empty slots into equipment matrix
    def load(self):
        type_index = 0

        for i in range(self.numRows):
            self.equipmentMatrix.append([])
            col_padding = (self.width - (self.numRomItems[i] * self.icon_width)) // (self.numRomItems[i] + 1)
            for j in range(self.numRomItems[i]):
                self.equipmentMatrix[i].append(Slot(self.slot_icon,
                                             i, j,
                                             self.icon_width, self.icon_height,
                                             ( (col_padding * (j+1)) + (self.icon_width * j),(self.slot_padding * (i+1)) + (self.icon_height * i)),
                                                    self.equipmentKeys[i]))

                self.equipmentMap[self.equipmentKeys[type_index]] = self.equipmentMatrix[i][j]
                type_index += 1


    def equip(self, item):
        self.equipmentMap[item.type].add(item)

        # if an object already exists in the designated slot, then swap
        # and return the object to inventory
        return

    def unfocus(self):
        self.isFocused = False
        self.selectedSlot = None

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

        self.hoverCursor()

        # draw slots and item icons
        for list in self.equipmentMatrix:
            for slot in list:
                slot.draw(self.surface)

    def hoverCursor(self):
        self.hoverSlot = self.equipmentMatrix[self.cursor_y][self.cursor_x]
        self.hoverSlot.hover = self.isFocused

    def moveCursor(self, left, down):
        if not self.isFocused:
            return

        self.hoverSlot.hover = False

        self.cursor_x = min(len(self.equipmentMatrix[self.cursor_y]) - 1, self.cursor_x + left) if left > 0 else max(0, self.cursor_x + left)
        self.cursor_y = min(len(self.equipmentMatrix) - 1, self.cursor_y + down) if down > 0 else max(0, self.cursor_y + down)