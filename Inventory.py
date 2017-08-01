from Slot import *

class Inventory:

    def __init__(self, frame_surface):
        self.frame = frame_surface
        self.capacity = INITIAL_INVENTORY_SIZE
        self.filledSlots = 0

        # size of slots shown to the user at a time (2 x 2 tiles)
        self.slotWidth = 5
        self.slotHeight = 3

        # index of the top left inventory of the viewing window
        self.curX = 0
        self.curY = 0

        self.itemMap = {}
        self.itemList = []

        # padding between each slot
        self.slotPadding = 10

        # inventory surfaces
        self.surface = pygame.Surface((FRAMEPIXELWIDTH, FRAMEPIXELHEIGHT))
        self.surface.set_alpha(MAX_ALPHA)

        self.gridtoframe_padding = 20
        self.inventory_grid = pygame.Surface((FRAMEPIXELWIDTH - self.gridtoframe_padding, (FRAMEPIXELHEIGHT // 2) - self.gridtoframe_padding))
        self.inventory_grid.fill((144, 144, 144))
        self.inventory_grid.set_alpha(MAX_ALPHA)

        self.icon_width = (FRAMEPIXELWIDTH - (self.slotWidth+1)*self.slotPadding - self.gridtoframe_padding) // self.slotWidth
        self.icon_height = self.icon_width
        self.slot_icon = imageLibrary.load(imageDirectory.slotIcon, self.icon_width, self.icon_height)

        self.load()

    # load in inventory images
    def load(self):
        self.background_image = Sprite(
            imageLibrary.staticLoad(imageDirectory.inventoryFrame,
                              FRAMEPIXELWIDTH,
                              FRAMEPIXELHEIGHT))

        # load itemList with empty slots
        num_rows = (self.capacity % self.slotWidth) + 1
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

        # draw the inventroy grid along with the items defined by curX and curY
        index= 0
        for list in range(self.curX, min(len(self.itemList), self.curX + self.slotHeight) ):
            for slot in range(self.curY, self.slotWidth):
                if index < self.capacity:
                    self.itemList[list][slot].draw(self.inventory_grid)
                else:
                    None
                    # draw greyed out square
                index += 1


    def increaseInventory(self, amount):
        # update capacity
        # add slots to itemList
        None

    def add(self, item):
        # check if item is already in inventory
        # if item.name in self.itemMap:

        # check if theres room to add new item
        if self.filledSlots+1 <= self.capacity:
            # add reference to itemMap
            # self.itemMap[item.name] = item

            self.filledSlots += 1

            for list in range(len(self.itemList)):
                # min check -> incase we wish to add a horizontal scroll in the future
                for slot in range(0, min(len(self.itemList[list]), self.slotWidth)):
                    if self.itemList[list][slot].isEmpty:
                        self.itemList[list][slot].item = item
                        self.itemList[list][slot].isEmpty = False
                        return True

        return False

    def remove(self, itemName=None, item=None, amount=-1):
        if itemName==None and item==None:
            return False

        # error check if the item is in itemMap
        # error check if filledSlots > 0

        name = itemName if item==None else item.name

        for list in reversed(xrange(len(self.itemList))):
            for slot in reversed(xrange(min(len(self.itemList[list]), self.slotWidth))):
                if not self.itemList[list][slot].isEmpty:
                    if self.itemList[list][slot].item.name == name:
                        # self.itemList[list][slot].itemStack = max(0, self.itemList[list][slot].itemStack - amount)
                        if amount == -1:
                            self.itemList[list][slot].isEmpty = True
                            self.itemList[list][slot].item = None
                            self.filledSlots =- 1

                        return True