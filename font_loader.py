from includes import *
#######################################################################################################################
#                                          Text Configurations
#######################################################################################################################
class fontLibrary:
    freesansbold = FONT_DIRECTORY + "freesansbold.ttf"

class textDef:
    font = pygame.font.Font(fontLibrary.freesansbold,20)
    font_size = font.get_height()