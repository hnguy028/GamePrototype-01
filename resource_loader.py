from functions import *

#######################################################################################################################
#                                          Text Configurations
#######################################################################################################################
class fontDirectory:
    freesansbold = FONT_DIRECTORY + "freesansbold.ttf"

class textDef:
    font = pygame.font.Font(fontDirectory.freesansbold,20)
    font_size = font.get_height()

#######################################################################################################################
#                                          Sprite Filename Definitions
#######################################################################################################################
class imageDirectory:

    mainmenu_background = MAIN_MENU_DIRECTORY + "cloud_scenery.jpg"
    mainmenu_floor = MAIN_MENU_DIRECTORY + "grass.png"
    mainmenu_castle = MAIN_MENU_DIRECTORY + "castle.png"
    mainmenu_cloud = MAIN_MENU_DIRECTORY + "cloud.png"

    lockedCharacter = MAIN_MENU_DIRECTORY + "shadow_char.png"
    knight = MAIN_MENU_DIRECTORY + "Knight01.png"

    promptFrame = MAIN_MENU_DIRECTORY + "testbg.png"
    selectHover = MAIN_MENU_DIRECTORY + "Hover.png"
    optionsButton = MAIN_MENU_DIRECTORY + "Options_Button.png"
    creditsButton = MAIN_MENU_DIRECTORY + "Credits_Button.png"
    deleteButton = MAIN_MENU_DIRECTORY + "Delete_Button.png"
    newGameButton = MAIN_MENU_DIRECTORY + "NewGame_Button.png"
    loadButton = MAIN_MENU_DIRECTORY + "LoadGame_Button.png"
    yesButton = MAIN_MENU_DIRECTORY + "Yes_Button.png"
    noButton = MAIN_MENU_DIRECTORY + "No_Button.png"

class imageLibrary:

    def __init__(self):
        self.imageDict = {}

    def load(self, imgfile, width=1, height=1, maximize=True):
        if imgfile in self.imageDict:
            return self.imageDict[imgfile]
        else:
            # load cloud images
            pre_surface = pygame.image.load(imgfile)

            # calculate aspect ratio
            aspect_ratio = scale_aspect(pre_surface.get_width(), pre_surface.get_height(), width, height, maximize)

            self.imageDict[imgfile] = pygame.transform.scale(
                pre_surface,
                (int(aspect_ratio[0]),int(aspect_ratio[1])))

            return self.imageDict[imgfile]

    def unload(self, imgfile):
        if imgfile in self.imageDict:
            del self.imageDict[imgfile]

#######################################################################################################################
#                                          Audio Definitions
#######################################################################################################################
class audioDirectory:
    mainmenu_music = AUDIO_DIRECTORY + "Journey_Soundtrack_Apotheosis.wav"


class audioLibrary:

    def __init__(self):
        self.audioDict = {}

    def load(self, audiofile):
        if audiofile in self.audioDict:
            return self.audioDict[audiofile]
        else:
            # load and store audio into dictionary
            self.audioDict[audiofile] = pygame.mixer.Sound(audiofile)

            return self.audioDict[audiofile]

    def unload(self, audiofile):
        if audiofile in self.audioDict:
            del self.audioDict[audiofile]


#######################################################################################################################
#                                          TileMap Filename Definitions
#######################################################################################################################
class tmxDirectory:
    None


#######################################################################################################################
#                                          Initialize Loader Objects
#######################################################################################################################
imageLibrary = imageLibrary()
audioLibrary = audioLibrary()