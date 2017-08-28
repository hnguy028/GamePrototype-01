from Player import *
from Options import *
from Inventory_Wallet import *
from datetime import datetime

class HUD:
    # initialize hud variables
    def __init__(self, north_dim, north_pos, south_dim, south_pos, player):
        self.n_width = north_dim[0]
        self.n_height = north_dim[1]
        self.north_pos = north_pos

        self.s_width = south_dim[0]
        self.s_height = south_dim[1]
        self.south_pos = south_pos

        # store references to player and inventory
        self.player = player
        self.inventory = player.inventory

        self.north_surface = pygame.Surface((self.n_width, self.n_height))
        self.south_surface = pygame.Surface((self.s_width, self.s_height))

    def draw(self, surface):
        # draw hud to frame
        surface.blit(self.north_surface, (self.north_pos))
        surface.blit(self.south_surface, (self.south_pos))

        # draw hud background
        self.north_surface.fill((144, 144, 144))
        self.south_surface.fill((144, 144, 144))

        text_padding = 10

        ################################## NORTH HUD #################################################################
        line = textDef.font.render(datetime.now().strftime("%I:%M"), option_ANITALIAS, (0, 0, 0, 0))
        self.north_surface.blit(line, ((self.n_width // 2) - (line.get_width() // 2), text_padding))

        line = textDef.font.render("Currecy: "  + str(self.inventory.wallet.getCurrency(Currency_Gold)), option_ANITALIAS, (0, 0, 0, 0))
        self.north_surface.blit(line, (self.n_width - (line.get_width() + text_padding), text_padding))

        ################################## SOUTH HUD #################################################################
        line = textDef.font.render("Health: " + str(self.player.health), option_ANITALIAS, (0, 0, 0, 0))
        self.south_surface.blit(line, (text_padding, text_padding))

        line = textDef.font.render("MP: " + str(self.player.magic), option_ANITALIAS, (0, 0, 0, 0))
        self.south_surface.blit(line, (self.s_width - (line.get_width() + text_padding), text_padding))

        line = textDef.font.render("Exp: " + str(self.player.experience) + " / 100", option_ANITALIAS, (0, 0, 0, 0))
        self.south_surface.blit(line, ((self.s_width // 2) - (line.get_width() // 2), self.s_height - line.get_height()))

        slot = self.inventory.get_HUD_slots()
        #slot_padding = (FRAMEPIXELWIDTH - len(slot) * slot.width) / (len(slot) + 1)
        slot.draw(self.south_surface, (self.s_width - (slot.width + text_padding), line.get_height() + text_padding))
