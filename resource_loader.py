from functions import *

#######################################################################################################################
#                                          Text Configurations
#######################################################################################################################
class fontDirectory:
    freesansbold = FONT_DIRECTORY + "freesansbold.ttf"
    allura_regular = FONT_DIRECTORY + "Allura-Regular.ttf"

class fontLibrary:
    def __init__(self):
        self.fontDict = {}
        self.staticFonts = {}

    def loadStatic(self, font, fontsize=20):
        if not font in self.staticFonts:
            self.staticFonts[font] = pygame.font.Font(font,fontsize)
        return self.staticFonts[font]

    def load(self, font, fontsize):
        self.fontDict[font] = pygame.font.Font(font, fontsize)
        return self.fontDict[font]


class textDef:
    font = pygame.font.Font(fontDirectory.freesansbold,20)
    font_size = font.get_height()

#######################################################################################################################
#                                          Sprite Filename Definitions
#######################################################################################################################
class imageDirectory:

    # Cursors
    cursor = UI_CURSOR_DIRECTORY + "cursor01.png"
    inventory_cursor = UI_CURSOR_DIRECTORY + "cursor05.png"

    # Main Menu Images
    mainmenu_castle = MAIN_MENU_DIRECTORY + "castle.png"
    mainmenu_cloud = MAIN_MENU_DIRECTORY + "cloud.png"
    mainmenu_background = MAIN_MENU_DIRECTORY + "cloud_scenery.jpg"
    mainmenu_floor = MAIN_MENU_DIRECTORY + "grass.png"
    lockedCharacter = MAIN_MENU_DIRECTORY + "locked_knight.png"
    knight = MAIN_MENU_DIRECTORY + "knight01.png"

    # Window Frames
    promptFrame = UI_COMPONENTS_DIRECTORY + "Prompt_Frame.png"
    inventoryFrame = UI_COMPONENTS_DIRECTORY + "Frame01.png"
    slotIcon = UI_COMPONENTS_DIRECTORY + "Slot01.png"

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

    # Items
    head_gear_test = COLLECTABLES_DIRECTORY + "head.png"
    weapon_test = COLLECTABLES_DIRECTORY + "sword.png"
    weapon_test02 = COLLECTABLES_DIRECTORY + "sword01.png"
    health_potion = COLLECTABLES_DIRECTORY + "health_potion.png"

class imageLibrary:

    def __init__(self):
        self.imageDict = {}
        self.staticImages = {}

    def load(self, imgfile, width=-1, height=-1, aspect=False, maximize=True):
        if not imgfile in self.imageDict:
            self.imageDict[imgfile] = pygame.image.load(imgfile)

        if width==-1 or height == -1:
            width = self.imageDict[imgfile].get_width()
            height = self.imageDict[imgfile].get_height()

        aspect_ratio = [width, height]

        if aspect:
            # calculate aspect ratio
            aspect_ratio = scale_aspect(self.imageDict[imgfile].get_width(), self.imageDict[imgfile].get_height(),
                                        width, height, maximize)

        return pygame.transform.scale(
            self.imageDict[imgfile],
            (int(aspect_ratio[0]),int(aspect_ratio[1])))

    def staticLoad(self, imgfile, width=0, height=0, aspect=False, maximize=True):
        if imgfile in self.staticImages:
            return self.staticImages[imgfile]
        else:
            self.staticImages[imgfile] = pygame.transform.scale(pygame.image.load(imgfile), (width, height))
            return self.staticImages[imgfile]

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
    SPAWN_CODE = 'spawn_point'
    IMPASSIVE_CODE = 'collidable'
    COLLECTABLE_CODE = 'collectables'

    # number of layers drawn
    DRAWN_LAYERS = 2

    META_LAYER = 2
    STRUCTURES_LAYER = 1
    GROUND_LAYER = 0

    # rgb color for meta layer collision
    META_RGB_FREE = (206,255,217,255)
    META_RGB_BINARY = ()
    META_RGB_MULTI = ()
    META_RGB_BLOCK = (255,206,206,255)
    META_RGB_SOLID = ()
    META_RGB_WATER = ()

    META_CODE_FREE = 'FREE'
    META_CODE_BINARY = ''
    META_CODE_MULTI = ''
    META_CODE_BLOCK = 'BLOCK'
    META_CODE_SOLID = 'SOLID'
    META_CODE_WATER = 'WATER'


#######################################################################################################################
#                                              Item Loader
#######################################################################################################################
class ItemDictionary:

    def __init__(self):
        self.items["bronze_sword"]

    def getValue(self, itemname):
        return self.items[itemname]

class AnimationLibrary:

    def __init__(self):
        self.boltAnim = pyganim.PygAnimation([(ATTACKS_DIRECTORY + 'bolt_strike_0001.png', 0.1),
                                         (ATTACKS_DIRECTORY + 'bolt_strike_0002.png', 0.1),
                                         (ATTACKS_DIRECTORY + 'bolt_strike_0003.png', 0.1),
                                         (ATTACKS_DIRECTORY + 'bolt_strike_0004.png', 0.1),
                                         (ATTACKS_DIRECTORY + 'bolt_strike_0005.png', 0.1),
                                         (ATTACKS_DIRECTORY + 'bolt_strike_0006.png', 0.1),
                                         (ATTACKS_DIRECTORY + 'bolt_strike_0007.png', 0.1),
                                         (ATTACKS_DIRECTORY + 'bolt_strike_0008.png', 0.1),
                                         (ATTACKS_DIRECTORY + 'bolt_strike_0009.png', 0.1),
                                         (ATTACKS_DIRECTORY + 'bolt_strike_0010.png', 0.1)])

#######################################################################################################################
#                                          Initialize Loader Objects
#######################################################################################################################
imageLibrary = imageLibrary()
audioLibrary = audioLibrary()
fontLibrary = fontLibrary()
animationLibrary = AnimationLibrary()
