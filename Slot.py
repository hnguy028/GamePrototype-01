from Item import *

class Slot:

    def __init__(self, image, xIndex, yIndex, width, height, pos):
        self.isEmpty = True
        self.item = None

        self.invIndexX = xIndex
        self.invIndexY = yIndex

        self.width = width
        self.height = height

        self.pos = pos

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 0, 0))

        self.background = image

    def draw(self, surface):
        # draw slot to inventory grid
        surface.blit(self.surface, self.pos)

        # draw item image to slot
        if not self.isEmpty:
            self.item.drawIcon(self.surface, (self.posX, self.posY))

            # draw stack number to corner of the slot if > 0