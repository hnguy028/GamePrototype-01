from Types import *
from resource_loader import *

# Displays currencies
class InventoryWallet:

    def __init__(self, width, height, pos=(0,0)):
        self.width = width
        self.height = height
        self.pos = pos

        self.surface = pygame.Surface((self.width, self.height))

        self.wallet = {}

        self.isFocused = False

        self.load()

    def load(self):
        # load currency mapping, init count to 0
        for currency in CurrencyTypes:
            self.wallet[currency] = 0

    def draw(self, surface, pos=(-1,-1)):
        drawPos = pos
        if drawPos == (-1, -1):
            drawPos = self.pos

        # draw wallet surface to inventory surface
        surface.blit(self.surface, drawPos)

        # draw background image to wallet surface
        self.surface.fill((144, 144, 144))

        i = 0
        for currency in CurrencyTypes:
            line = textDef.font.render(currency + ": "  + str(self.wallet[currency]), False, (0, 0, 0, 0))
            self.surface.blit(line, (self.width//2, self.height//2 + i))
            i += 25

    def getCurrency(self, currency_type):
        if currency_type in CurrencyTypes:
            return self.wallet[currency_type]

    def add(self, currency, amount=1):
        self.wallet[currency] += amount

    # TODO: should it take an item or amount (possible have 2 subtract methods)
    def subtract(self):
        return False

    def unfocus(self):
        self.isFocused = False

