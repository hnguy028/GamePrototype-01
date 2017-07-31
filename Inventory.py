from Slot import *

class Inventory:

    def __init__(self, frame_surface):
        self.maxSlots = 13
        self.frame = frame_surface

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
        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(MAX_ALPHA)

        self.inventory_grid = pygame.Surface((FRAMEPIXELWIDTH, FRAMEPIXELHEIGHT - 100))
        self.inventory_grid.fill((255, 255, 255))
        self.inventory_grid.set_alpha(MAX_ALPHA)

        self.icon_width = (FRAMEPIXELWIDTH - (self.slotWidth+1)*self.slotPadding) // self.slotWidth
        self.icon_height = self.icon_width
        #self.slot_icon = imageLibrary.load(imageDirectory.slotIcon, self.icon_width, self.icon_height)
        self.slot_icon = None

        self.load()

    # load in inventory images
    def load(self):
        #self.background_image = Sprite(
        #    imageLibrary.load(imageDirectory.inventoryFrame,
        #                      FRAMEWIDTH,
        #                      FRAMEPIXELHEIGHT))

        # load itemList with empty slots
        num_rows = (self.maxSlots % self.slotWidth) + 1
        num_cols = self.slotWidth
        index = 0
        for i in range(num_rows):
            self.itemList.append([])
            for j in range(num_cols):
                if index < self.maxSlots:
                    self.itemList[i].append(Slot(self.slot_icon,
                                               i, j,
                                               self.icon_width, self.icon_height,
                                               ( (self.slotPadding * (j+1)) + (self.icon_width * j),(self.slotPadding * (i+1)) + (self.icon_height * i))))
                    index += 1
                else:
                    break

    def draw(self):
        # draw frame background image
        #self.surface.blit(self.background_image, (0,0))
        self.surface.fill((0, 0, 0))

        # draw the unique currencies, and the inventroy title

        # draw the inventroy grid along with the items defined by curX and curY
        for list in range(self.curX, min(len(self.itemList), self.curX + self.slotHeight) ):
            for slot in range(self.curY, self.slotWidth):
                self.itemList[list][slot].draw(self.inventory_grid)

        # draw inventory grid to surface
        self.surface.blit(self.inventory_grid, (0,25))

        # draw surface to frame
        self.frame.blit(self.surface, (0, 0))


    def add(self, item):
        None

    def remove(self, x, y):
        None
