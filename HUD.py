from Player import *
from Inventory_Wallet import *

class HUD:
    # initialize hud variables
    def __init__(self, width, height, pos, player):
        self.width = width
        self.height = height
        self.pos = pos

        # store references to player and inventory
        self.player = player
        self.inventory = player.inventory

        self.surface = pygame.Surface((width, height))

    def initHUD(self):
        print("Init HUD")

    def draw(self, surface):
        # draw hud to frame
        surface.blit(self.surface, (self.pos))

        # draw hud background
        self.surface.fill((144, 144, 144))

        text_padding = 10

        line = textDef.font.render("Health: " + str(self.player.health), False, (0, 0, 0, 0))
        self.surface.blit(line, (text_padding, text_padding))

        line = textDef.font.render("MP: " + str(self.player.magic), False, (0, 0, 0, 0))
        self.surface.blit(line, (text_padding, text_padding * 2 + line.get_height()))

        line = textDef.font.render("Exp: " + str(self.player.experience) + " / 100", False, (0, 0, 0, 0))
        self.surface.blit(line, (text_padding, text_padding * 3 + line.get_height() * 2))

        line = textDef.font.render("Gold: "  + str(self.inventory.wallet.getCurrency(Currency_Gold)), False, (0, 0, 0, 0))
        self.surface.blit(line, (self.width - (line.get_width() + text_padding), text_padding))

        slot = self.inventory.getEquiped()
        slot.draw(self.surface, (self.width - (slot.width + text_padding), line.get_height() + text_padding * 2))
