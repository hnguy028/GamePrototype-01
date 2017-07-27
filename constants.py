# Global Constants & Variable definition

GAME_TITLE = 'Loot 2D'
GAME_ICON = 'resources/menu_sprites/icon.png'

RESOURCE_DIRECTORY = 'resources/'


CHARACTER_DIRECTORY = RESOURCE_DIRECTORY + 'characters/'
COLLECTABLES_DIRECTORY = RESOURCE_DIRECTORY + 'collectables/'
MAPS_DIRECTORY = RESOURCE_DIRECTORY + 'maps/'
MAIN_MENU_DIRECTORY = RESOURCE_DIRECTORY + 'menu_sprites/'
FONT_DIRECTORY = RESOURCE_DIRECTORY + 'fonts/'
SAVE_DIRECTORY = RESOURCE_DIRECTORY + 'saves/'

########## Character Information
CHARACTER_NAME = "link"
CHAR_WALKRATE = 10
CHAR_RUNRATE = 20


# Character orientation variables
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

CHARACTER_WIDTH = 0
CHARACTER_HEIGHT = 0

# TMX object codes
SPAWN_CODE = 'SpawnPoint'
IMPASSIVE_CODE = 'collidable'
COLLECTABLE_CODE = 'collectables'

# Window variables
# Tile size in pixels
TILESIZE = 32

# Size of the window frame in (32 x 32) tiles
FRAMEWIDTH = 15
FRAMEHEIGHT = 19

FRAMEPIXELWIDTH = FRAMEWIDTH * TILESIZE
FRAMEPIXELHEIGHT = FRAMEHEIGHT * TILESIZE

# Size of the room frame in (32 x 32) tiles
ROOMWIDTH = 15
ROOMHEIGHT = 15

# Size of the hud in (32 x 32) tiles
HUDSIZE_TOP = 1
HUDSIZE_BOTTOM = 4

#######################################################################################################################
#                                          Sprite Filename Definitions
#######################################################################################################################
class imageLibrary:
    mainmenu_background = MAIN_MENU_DIRECTORY + "cloud_scenery.jpg"
    mainmenu_floor = MAIN_MENU_DIRECTORY + "grass.png"
    mainmenu_castle = MAIN_MENU_DIRECTORY + "castle.png"
    mainmenu_cloud = MAIN_MENU_DIRECTORY + "cloud.png"

    lockedCharacter = MAIN_MENU_DIRECTORY + "shadow_char.png"
    knight = MAIN_MENU_DIRECTORY + "Knight01.png"

    promptFrame = MAIN_MENU_DIRECTORY + "testbg.png"
    optionsButton = MAIN_MENU_DIRECTORY + "Options_Button.png"
    creditsButton = MAIN_MENU_DIRECTORY + "Credits_Button.png"
    deleteButton = MAIN_MENU_DIRECTORY + "Delete_Button.png"
    newGameButton = MAIN_MENU_DIRECTORY + "NewGame_Button.png"
    loadButton = MAIN_MENU_DIRECTORY + "LoadGame_Button.png"
    yesButton = MAIN_MENU_DIRECTORY + "Yes_Button.png"
    noButton = MAIN_MENU_DIRECTORY + "No_Button.png"

#######################################################################################################################
#                                          TileMap Filename Definitions
#######################################################################################################################
class tmxLibrary:
    None