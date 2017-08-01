from Item import *

class Slot:

    def __init__(self, image, xIndex, yIndex, width, height, pos):
        self.isEmpty = True
        self.item = None
        self.itemStack = 0

        self.invIndexX = xIndex
        self.invIndexY = yIndex

        self.width = width
        self.height = height

        self.pos = pos

        self.itemPadding = 10

        self.surface = pygame.Surface((self.width, self.height))

        self.background = image

    def draw(self, surface):
        # draw slot to inventory grid
        surface.blit(self.surface, self.pos)

        # draw background image
        self.surface.blit(self.background, (0, 0))

        # draw item image to slot
        if not self.isEmpty:
            self.item.draw(self.surface, self.width - (2 * self.itemPadding), self.height - (2 * self.itemPadding), (self.itemPadding, self.itemPadding))

            # draw stack number to corner of the slot if > 0