# Global Constants & Variable definition

GAME_TITLE = 'Loot 2D'
GAME_ICON = 'resources/ui_sprites/icon.png'

RESOURCE_DIRECTORY = 'resources/'
UI_DIRECTORY = RESOURCE_DIRECTORY + 'ui_sprites/'

CHARACTER_DIRECTORY = RESOURCE_DIRECTORY + 'characters/'
COLLECTABLES_DIRECTORY = RESOURCE_DIRECTORY + 'items/'
MAPS_DIRECTORY = RESOURCE_DIRECTORY + 'maps/'
FONT_DIRECTORY = RESOURCE_DIRECTORY + 'fonts/'
AUDIO_DIRECTORY = RESOURCE_DIRECTORY + 'audio/'
SAVE_DIRECTORY = RESOURCE_DIRECTORY + 'saves/'

MAIN_MENU_DIRECTORY = UI_DIRECTORY + 'mainmenu/'
UI_COMPONENTS_DIRECTORY = UI_DIRECTORY + 'components/'
UI_CURSOR_DIRECTORY = UI_DIRECTORY + 'cursor/'


########## Game Information
FPS = 30

########## Character Information
CHARACTER_NAME = "link"
CHAR_WALKRATE = 10
CHAR_RUNRATE = 20

######### Inventory Defaults
INITIAL_INVENTORY_SIZE = 13
DEFAULT_INV_GRID_WIDTH = 5
DEFAULT_INV_GRID_HEIGHT = 3

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


# Size of the hud in (32 x 32) tiles
HUDSIZE_TOP = 1
HUDSIZE_BOTTOM = 4

# Size of the window frame in (32 x 32) tiles
FRAMEWIDTH = 15
FRAMEHEIGHT = 15 + HUDSIZE_BOTTOM

FRAMEPIXELWIDTH = FRAMEWIDTH * TILESIZE
FRAMEPIXELHEIGHT = FRAMEHEIGHT * TILESIZE

# Size of the room frame in (32 x 32) tiles
ROOMWIDTH = 15
ROOMHEIGHT = 15

MAX_ALPHA = 255
MIN_ALPHA = 0