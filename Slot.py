from Item import *

class Slot:

    def __init__(self, image, xIndex, yIndex, width, height, pos, type=None):
        self.isEmpty = True
        self.item = None
        self.itemStack = 0
        self.hover = False
        self.isSelected = False
        self.type = type

        self.invIndexX = xIndex
        self.invIndexY = yIndex

        self.width = width
        self.height = height

        self.pos = pos

        self.itemPadding = 10

        self.surface = pygame.Surface((self.width, self.height))

        self.background = image

    def add(self, item, amount=1):
        if not self.isEmpty:
            self.itemStack += amount
        else:
            self.item = item
            self.isEmpty = False
            self.itemStack += amount

    def remove(self, amount=1):
        self.itemStack -= amount

        if amount < 0 or self.itemStack <= 0:
            self.item = None
            self.isEmpty = True
            self.itemStack = 0

        return self.itemStack == 0

    # swaps item between slots, if input slot is empty then move current item there
    def swap(self, slot):
        if not self.isEmpty:
            slot.isEmpty, self.isEmpty = self.isEmpty, slot.isEmpty
            slot.itemStack, self.itemStack = self.itemStack, slot.itemStack
            slot.item, self.item = self.item, slot.item


    # TODO : split a stack in 2 into input slot
    def split(self, slot, amount):
        None

    def draw(self, surface):
        # draw slot to inventory grid
        surface.blit(self.surface, self.pos)

        # draw background image
        self.surface.blit(self.background, (0, 0))

        # draw item image to slot
        if not self.isEmpty:
            self.item.draw(self.surface, self.width - (2 * self.itemPadding), self.height - (2 * self.itemPadding), (self.itemPadding, self.itemPadding))

            # draw stack size to corner of the slot
            if self.itemStack > 1:
                num = textDef.font.render(str(self.itemStack), False, (0, 0, 0, 0))
                self.surface.blit(num, (self.itemPadding, self.itemPadding))

        if self.hover:
            self.surface.blit(imageLibrary.staticLoad(imageDirectory.cursor), (self.width // 2, self.height // 2))