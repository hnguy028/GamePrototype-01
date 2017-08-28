from Slot import *

# Equipment class holds information of items, and abilities currently equiped to the player
class InventoryEquipment:

    def __init__(self, width, height, slot_icon, icon_width, icon_height, slot_padding, pos=(0, 0)):

        self.width = width
        self.height = height
        self.pos = pos

        self.surface = pygame.Surface((self.width, self.height))

        self.equipmentKeys = ["left_hand", "accessory1", "ammunition", "potion", "right_hand", "head_gear", "chest_gear", "waist_gear", "leg_gear", "feet_gear"]

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


    # amount is intended to change only for ammunition
    def equip(self, item, amount=1):
        if self.equipmentMap[item.type].isEmpty:
            # if nothing is equip add to designated item slot
            self.equipmentMap[item.type].add(item)

            return None, None
        else:
            # if an object already exists in the designated slot, then swap
            rtn_item, rtn_amount = self.equipmentMap[item.type].swap_item(item, amount)

            # retun the item to inventory
            return rtn_item, rtn_amount

    def equip_slot(self, slot):
        if not slot.isEmpty:
            self.equipmentMap[slot.item.type].swap(slot)

    def unequip(self):
        # removes and returns the item, and number of items in the slot
        return self.equipmentMatrix[self.cursor_x][self.cursor_y].remove(-1)

    def unfocus(self):
        self.isFocused = False
        self.selectedSlot = None

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

        self.hoverCursor()