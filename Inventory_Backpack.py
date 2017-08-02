from Slot import *

class InventoryBackpack:

    def __init__(self, width, slot_icon, icon_width, icon_height, slot_padding, pos=(0, 0)):
        self.capacity = 25
        self.filledSlots = 0

        # size of slots shown to the user at a time
        self.slotWidth = DEFAULT_INV_GRID_WIDTH
        self.slotHeight = DEFAULT_INV_GRID_HEIGHT

        # index of the top left inventory of the viewing window
        self.inv_gridX = 0
        self.inv_gridY = 0

        self.itemMap = {}
        self.itemList = []

        self.slot_icon = slot_icon
        self.icon_width = icon_width
        self.icon_height = icon_height
        self.slot_padding = slot_padding

        self.width = width
        self.height = self.icon_height * self.slotHeight  + self.slot_padding * (self.slotHeight+1)
        self.pos = pos

        self.surface = pygame.Surface((self.width, self.height))

        self.itemMap = {}
        self.itemList = []

        self.cursor_x = 0
        self.cursor_y = 0
        self.hoverSlot = None
        self.selectedSlot = None

        self.isFocused = False

        self.load()

    # load itemlist with empty slots
    def load(self):
        num_rows = (self.capacity // self.slotWidth) + 1
        num_cols = self.slotWidth
        index = 0
        for i in range(num_rows):
            self.itemList.append([])
            for j in range(num_cols):
                if index < self.capacity:
                    self.itemList[i].append(Slot(self.slot_icon,
                                               i, j,
                                               self.icon_width, self.icon_height,
                                               ( (self.slot_padding * (j+1)) + (self.icon_width * j),(self.slot_padding * (i+1)) + (self.icon_height * i))))
                    index += 1
                else:
                    break

    def draw(self, surface, pos=(-1,-1)):
        drawPos = pos
        if drawPos == (-1,-1):
            drawPos = self.pos

        # draw backpack to inventory surface
        surface.blit(self.surface, drawPos)

        # draw background image to backpacki surface
        self.surface.fill((144, 144, 144))

        # cursor
        self.hoverCursor()

        # draw the backpack grid along with the items defined by curX and curY
        index = 0
        for list in range(self.inv_gridY, self.inv_gridY + self.slotHeight ):
            for slot in range(self.inv_gridX, self.slotWidth):
                if index < self.capacity:
                    self.itemList[list][slot].draw(self.surface)
                else:
                    # draw greyed out square
                    None
                    # break for now
                    break
                index += 1

    def unfocus(self):
        self.isFocused = False
        self.selectedSlot = None

    def hoverCursor(self):
        self.hoverSlot = self.itemList[self.cursor_y][self.cursor_x]
        self.hoverSlot.hover = self.isFocused

    def moveCursor(self, left=0, down=0):
        if not self.isFocused:
            return

        self.hoverSlot.hover = False

        self.cursor_x = min(len(self.itemList[self.cursor_y] ) - 1, self.cursor_x + left) if left > 0 else max(0, self.cursor_x + left)

        # moving up
        if down < 0:
            #self.scroll(down)
            self.cursor_y = max(0, self.cursor_y + down)

        # moving down
        elif down > 0:
            #self.scroll(down)
            self.cursor_y = min(self.slotHeight - 1, self.cursor_y + down)
            self.cursor_x = min(len(self.itemList[self.cursor_y] ) - 1, self.cursor_x)

    # TODO : slots are fixed so this wont work
    def scroll(self, down):
        if down < 0:
            self.inv_gridY = max(0, self.inv_gridY + down)
        elif down > 0:
            self.inv_gridY = min(len(self.itemList) - 1, self.inv_gridY + down)

    def increaseCapacity(self, amount):
        index, self.capacity = self.capacity, self.capacity + amount
        num_rows = (self.capacity // self.slotWidth) + 2
        num_cols = self.slotWidth

        # fill any horizontal spaces
        last_pack_index = len(self.itemList) - 1
        for k in range(len(self.itemList[last_pack_index]), num_cols):
            if index < self.capacity:
                self.itemList[last_pack_index].append(Slot(self.slot_icon,
                                             last_pack_index, k,
                                             self.icon_width, self.icon_height,
                                             ((self.slot_padding * (k + 1)) + (self.icon_width * k),
                                              (self.slot_padding * (last_pack_index + 1)) + (self.icon_height * last_pack_index))))
                index += 1
            else:
                return

        # otherwise add more rows
        for i in range(len(self.itemList), num_rows):
            self.itemList.append([])
            for j in range(0, num_cols):
                if index < self.capacity:
                    self.itemList[i].append(Slot(self.slot_icon,
                                               i, j,
                                               self.icon_width, self.icon_height,
                                               ( (self.slot_padding * (j+1)) + (self.icon_width * j),(self.slot_padding * (i+1)) + (self.icon_height * i))))
                    index += 1
                else:
                    return

    def selectSlot(self):
        if self.selectedSlot == None:
            if not self.itemList[self.cursor_y][self.cursor_x].isEmpty:
                self.selectedSlot = self.itemList[self.cursor_y][self.cursor_x]
        else:
            item = self.selectedSlot.item
            self.selectedSlot.swap(self.itemList[self.cursor_y][self.cursor_x])

            # update item mapping
            self.itemMap[item.name] = self.itemList[self.cursor_y][self.cursor_x]
            if not self.selectedSlot.isEmpty:
                self.itemMap[self.selectedSlot.item.name] = self.selectedSlot

            self.releaseSelect()

    def equip(self, equipment):
        if not self.itemList[self.cursor_y][self.cursor_x].isEmpty:
            equipment.equip()


    def releaseSelect(self):
        self.selectedSlot = None

    def add(self, item):
        # check if item is already in backpack
        if item.name in self.itemMap:
           self.itemMap[item.name].itemStack += 1
           return True

        # check if theres room to add new item
        if self.filledSlots+1 <= self.capacity:

            self.filledSlots += 1

            for list in range(len(self.itemList)):
                # min check -> incase we wish to add a horizontal scroll in the future
                for slot in range(0, min(len(self.itemList[list]), self.slotWidth)):
                    if self.itemList[list][slot].isEmpty:
                        self.itemList[list][slot].add(item)
                        self.itemMap[item.name] = self.itemList[list][slot]
                        return True
        return False

    def remove(self, itemName=None, item=None, amount=1):
        # extract name
        name = itemName if item == None else item.name

        if name == None:
            return False

        if name in self.itemMap:
            if self.itemMap[name].remove(amount):
                del self.itemMap[name]

            return True

        return False

    def removeSelected(self, amount=1):
        if not self.selectedSlot.isEmpty:
            if self.selectedSlot.remove(amount):
                del self.itemMap[self.selectedSlot.item.name]

    def removeLast(self, itemName=None, item=None, amount=1):
        name = itemName if item == None else item.name

        if name == None:
            return False

        for list in reversed(range(len(self.itemList))):
            for slot in reversed(range(min(len(self.itemList[list]), self.slotWidth))):
                if not self.itemList[list][slot].isEmpty:
                    if self.itemList[list][slot].item.name == name:
                        if amount == -1:
                            self.itemList[list][slot].remove(amount)
                            self.filledSlots -= 1
                            del self.itemMap[list][slot]
                        else:
                            self.itemList[list][slot].remove(amount)

                        return True