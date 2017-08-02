from Equipment import *

class Inventory:

    def __init__(self, frame_surface):
        self.frame = frame_surface
        self.capacity = 13
        self.filledSlots = 0

        # size of slots shown to the user at a time (2 x 2 tiles)
        self.slotWidth = 5
        self.slotHeight = 3

        # index of the top left inventory of the viewing window
        self.inv_gridX = 0
        self.inv_gridY = 0

        self.itemMap = {}
        self.itemList = []

        # padding between each slot
        self.slotPadding = 10

        # inventory surfaces
        self.surface = pygame.Surface((FRAMEPIXELWIDTH, FRAMEPIXELHEIGHT))
        self.surface.set_alpha(MAX_ALPHA)

        # inventroy grid
        self.gridtoframe_padding = 5
        self.inventory_grid = pygame.Surface((FRAMEPIXELWIDTH - self.gridtoframe_padding, FRAMEPIXELHEIGHT - 200))
        self.inventory_grid.fill((144, 144, 144))
        self.inventory_grid.set_alpha(MAX_ALPHA)

        # icon size configurations
        self.icon_width = (FRAMEPIXELWIDTH - (self.slotWidth+1)*self.slotPadding - self.gridtoframe_padding) // self.slotWidth
        self.icon_height = self.icon_width
        self.slot_icon = imageLibrary.load(imageDirectory.slotIcon, self.icon_width, self.icon_height)

        # load inventory
        self.load()

        # initialize and load equipment
        self.equipment = Equipment(FRAMEPIXELWIDTH - self.gridtoframe_padding, self.icon_height*2 + self.slotPadding*3 ,
                                   self.slot_icon, self.icon_width, self.icon_height, self.slotPadding)

        # reference to the selected slot, to either move, equip, or swap
        self.selectedSlot = None

        # cursor position
        self.cursor_x = 0
        self.cursor_y = 0
        self.hoverSlot = None
        self.cursor_panel = InventoryPanel.INVENTORY
        self.cursor_image = imageLibrary.load(imageDirectory.cursor, 30, 30, True)


    # load in inventory images
    def load(self):
        self.background_image = Sprite(
            imageLibrary.staticLoad(imageDirectory.inventoryFrame,
                              FRAMEPIXELWIDTH,
                              FRAMEPIXELHEIGHT))

        # load itemList with empty slots
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
                                               ( (self.slotPadding * (j+1)) + (self.icon_width * j),(self.slotPadding * (i+1)) + (self.icon_height * i))))
                    index += 1
                else:
                    break

    def draw(self):
        # draw inventory surface to frame
        self.frame.blit(self.surface, (0, 0))

        # draw background image to inventory surface
        self.background_image.draw(self.surface)

        # draw inventory grid to inventory surface
        self.surface.blit(self.inventory_grid, (self.gridtoframe_padding // 2, self.gridtoframe_padding))

        # draw the unique currencies, and the inventroy title

        # cursor
        self.hoverCursor()

        # draw the inventroy grid along with the items defined by curX and curY
        index= 0
        for list in range(self.inv_gridX, min(len(self.itemList), self.inv_gridX + self.slotHeight) ):
            for slot in range(self.inv_gridY, self.slotWidth):
                if index < self.capacity:
                    self.itemList[list][slot].draw(self.inventory_grid)
                else:
                    None
                    # draw greyed out square
                index += 1

        # draw equipment
        self.equipment.draw(self.surface, (self.gridtoframe_padding // 2, FRAMEPIXELHEIGHT - (self.icon_height*2 + self.slotPadding*3 + self.gridtoframe_padding)))

    def hoverCursor(self):
        if self.cursor_panel == InventoryPanel.INVENTORY:
            self.hoverSlot = self.itemList[self.cursor_y][self.cursor_x]
        elif self.cursor_panel == InventoryPanel.EQUIPMENT:
            self.hoverSlot = self.equipment.equipmentMatrix[self.cursor_y][self.cursor_x]

        self.hoverSlot.hover = True


    def moveCursor(self, left=0, down=0):
        self.hoverSlot.hover = False

        if self.cursor_panel == InventoryPanel.INVENTORY:
            self.cursor_x = min(self.slotWidth - 1, self.cursor_x + left) if left > 0 else max(0, self.cursor_x + left)

            # check if we can scroll

            if down < 0:
                self.cursor_y = max(0, self.cursor_y + down)
            elif down > 0:
                self.cursor_y = min(self.slotHeight - 1, self.cursor_y + down)
                self.cursor_x = min(len(self.itemList[self.cursor_y] ) - 1, self.cursor_x)

        elif self.cursor_panel == InventoryPanel.EQUIPMENT:
            self.cursor_x, self.cursor_y = self.equipment.move(self.cursor_x, self.cursor_y, left, down)


    def scroll(self):
        None
        #self.inventory_grid.scroll(0, self.slotHeight + self.slotPadding)

    def increaseInventory(self, amount):
        # update capacity
        # add slots to itemList
        None

    def selectSlot(self):
        if self.selectedSlot == None:
            if self.cursor_panel == InventoryPanel.INVENTORY:
                self.selectedSlot = self.itemList[self.cursor_y][self.cursor_x]
            elif self.cursor_panel == InventoryPanel.EQUIPMENT:
                self.selectedSlot = self.equipment.equipmentMatrix  [self.cursor_y][self.cursor_x]
        else:
            item = self.selectedSlot.item
            self.selectedSlot.swap(self.itemList[self.cursor_y][self.cursor_x])

            # update item mapping
            self.itemMap[item.name] = self.itemList[self.cursor_y][self.cursor_x]

            self.releaseSelect()

    def releaseSelect(self):
        self.selectedSlot = None

    def add(self, item):
        # check if item is already in inventory
        if item.name in self.itemMap:
           self.itemMap[item.name].itemStack += 1
           return True

        # check if theres room to add new item
        if self.filledSlots+1 <= self.capacity:
            # add reference to itemMap
            # self.itemMap[item.name] = item

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

        # check if inventroy size > 0 or item is in itemMap
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

class InventoryPanel:
    INVENTORY, EQUIPMENT = range(2)