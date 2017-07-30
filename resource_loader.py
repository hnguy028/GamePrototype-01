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

    # Cursors
    cursor = UI_CURSOR_DIRECTORY + "cursor01.png"

    # Main Menu Images
    mainmenu_castle = MAIN_MENU_DIRECTORY + "castle.png"
    mainmenu_cloud = MAIN_MENU_DIRECTORY + "cloud.png"
    mainmenu_background = MAIN_MENU_DIRECTORY + "cloud_scenery.jpg"
    mainmenu_floor = MAIN_MENU_DIRECTORY + "grass.png"
    lockedCharacter = MAIN_MENU_DIRECTORY + "locked_knight.png"
    knight = MAIN_MENU_DIRECTORY + "knight01.png"

    # Window Frames
    promptFrame = UI_COMPONENTS_DIRECTORY + "Grey_Frame.png"

    # Buttons
    selectHover = UI_COMPONENTS_DIRECTORY + "Hover.png"
    blankButton = UI_COMPONENTS_DIRECTORY + "Blank_Button.png"
    controlSettingsButton = UI_COMPONENTS_DIRECTORY + "Controls_Button.png"
    optionsButton = UI_COMPONENTS_DIRECTORY + "Options_Button.png"
    creditsButton = UI_COMPONENTS_DIRECTORY + "Credits_Button.png"
    deleteButton = UI_COMPONENTS_DIRECTORY + "Delete_Button.png"
    newGameButton = UI_COMPONENTS_DIRECTORY + "NewGame_Button.png"
    loadButton = UI_COMPONENTS_DIRECTORY + "Load_Button.png"
    confirmButton = UI_COMPONENTS_DIRECTORY + "Confirm_Button.png"
    cancelButton = UI_COMPONENTS_DIRECTORY + "Cancel_Button.png"

class imageLibrary:

    def __init__(self):
        self.imageDict = {}

    def load(self, imgfile, width=10, height=10, aspect=False, maximize=True):
        if imgfile in self.imageDict:
            return self.imageDict[imgfile]
        else:
            # load cloud images
            pre_surface = pygame.image.load(imgfile)

            aspect_ratio = [width, height]

            if aspect:
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
    credit_music = AUDIO_DIRECTORY + "TroyBoi_-_On_My_Own_feat_Nefera_.wav"


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


# TMX object codes
class tmxCodes:
    SPAWN_CODE = 'SpawnPoint'
    IMPASSIVE_CODE = 'collidable'
    COLLECTABLE_CODE = 'collectables'

    DRAWN_LAYERS = 2

    META_LAYER = 2
    STRUCTURES_LAYER = 1
    GROUND_LAYER = 0


#######################################################################################################################
#                                          Initialize Loader Objects
#######################################################################################################################
imageLibrary = imageLibrary()
audioLibrary = audioLibrary()