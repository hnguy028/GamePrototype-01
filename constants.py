# Global Constants & Variable definition

GAME_TITLE = 'Loot 2D'
GAME_ICON = 'resources/menu_sprites/icon.png'

RESOURCE_DIRECTORY = 'resources/'


CHARACTER_DIRECTORY = RESOURCE_DIRECTORY + 'characters/'
COLLECTABLES_DIRECTORY = RESOURCE_DIRECTORY + 'collectables/'
MAPS_DIRECTORY = RESOURCE_DIRECTORY + 'maps/'
MAIN_MENU_DIRECTORY = RESOURCE_DIRECTORY + 'menu_sprites/'
FONT_DIRECTORY = RESOURCE_DIRECTORY + 'fonts/'
AUDIO_DIRECTORY = RESOURCE_DIRECTORY + 'audio/'
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

#
MAX_ALPHA = 255
MIN_ALPHA = 0