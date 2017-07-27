from GameClasses import *
from includes import *
from constants import *
from functions import *
import copy

class gameEngine:

    def __init__(self):
        # Init main menu variables
        self.frameLoaded = False
        self.mainMenuLoaded = False
        self.gameLoaded = False

        self.mm_clouds = []
        self.mm_character_loadout = []
        self.mm_character_saves = []
        self.mm_character_selected = None
        self.mm_character_index = 0

    def loadSurface(self):
        if not self.frameLoaded:
            self.frameLoaded = True
            self.WORLD = WindowSurface(HUDSIZE_BOTTOM, ROOMWIDTH, ROOMHEIGHT)

    # Load Game State classes
    def loadGame(self):
        if not self.gameLoaded:
            self.gameLoaded = True
            self.ROOM = RoomSurface("desert_world2")
            self.PLAYER = Player(self.ROOM, self.ROOM.playerSpawn, CHARACTER_NAME, 100, 100, 100, DOWN)
            self.HUD = HUD()

            self.ROOM.loadMap()

    # load main menu state classes and images
    def load_mainmenu(self):
        if not self.mainMenuLoaded:
            self.mainMenuLoaded = True

            # load in castle image and scale to the frame
            self.mmCastle = pygame.transform.scale(
                pygame.image.load(MAIN_MENU_DIRECTORY + 'castle.png'),
                    (TILESIZE * FRAMEWIDTH,
                     TILESIZE * (FRAMEHEIGHT - int(FRAMEHEIGHT * 0.1))))

            # Main Menu Background Image
            self.mmBackground = pygame.transform.scale(
                pygame.image.load(MAIN_MENU_DIRECTORY + 'cloud_scenery.jpg'),
                    (TILESIZE * FRAMEWIDTH,
                     TILESIZE * (FRAMEHEIGHT - int(FRAMEHEIGHT * 0.2))))

            # Background Floor Image
            self.mmBgFloor = pygame.transform.scale(
                pygame.image.load(MAIN_MENU_DIRECTORY + 'grass.png'),
                    (TILESIZE * FRAMEWIDTH,
                     TILESIZE * (FRAMEHEIGHT - int(FRAMEHEIGHT * 0.6))))

            # Locked Character Image
            self.mmLockedCharacter_Knight = pygame.transform.scale(
                pygame.image.load(MAIN_MENU_DIRECTORY + 'shadow_char.png'),
                (50, 100))

            for i in range(4):
                self.mm_character_loadout.append(self.mmLockedCharacter_Knight)
                self.mm_character_saves.append(GameSaves(i, self.mmLockedCharacter_Knight, ""))

            self.mm_character_selected = pygame.transform.scale(
                pygame.image.load(MAIN_MENU_DIRECTORY + 'Knight01.png'),
                (50, 100))

            self.mm_character_loadout[0] = self.mm_character_selected

            # Load Character from file if it exists
            for i in range(4):
                try:
                    file = open(SAVE_DIRECTORY + 'savefile_0' + str(i), 'r')
                    char_name = file.readline()

                    loaded_character = pygame.transform.scale(
                        pygame.image.load(MAIN_MENU_DIRECTORY + char_name),
                        (50, 100))

                    self.mm_character_saves[i] = GameSaves(i, loaded_character, SAVE_DIRECTORY + 'savefile_0' + str(i), False)

                    file.close()
                except Exception:
                    None # Do nothing

            # calculate the equal distance between each character position
            char_margin = TILESIZE * FRAMEWIDTH / 8
            posCorrection = self.mmLockedCharacter_Knight.get_width() / 2
            self.charPosition = [char_margin - posCorrection,
                                 (char_margin*3) - posCorrection,
                                 (char_margin*5) - posCorrection,
                                 (char_margin*7) - posCorrection]

            # load cloud images
            loaded_cloud = pygame.image.load(MAIN_MENU_DIRECTORY + 'cloud.png')

            # calculate aspect ratio
            aspect_ratio = scale_aspect(loaded_cloud.get_width(), loaded_cloud.get_height(), 270, 170, False)

            # scale image
            self.mmCloud01 = pygame.transform.scale(
                loaded_cloud,
                (int(aspect_ratio[0]),int(aspect_ratio[1])))

            mmCloudWidth = self.mmCloud01.get_width()

            # generate random cloud locations, and movement speeds
            for i in range(1, random.randrange(3, 5)):
                speed = random.randrange(-2, 2)

                if speed == 0:
                    speed += 1

                xpos = random.randrange(mmCloudWidth, mmCloudWidth+50)

                if speed < 0:
                    xpos += (FRAMEWIDTH * TILESIZE)
                else:
                    xpos = -xpos

                # add the cloud to list of clouds to be drawn
                self.mm_clouds.append(
                    Cloud(self.mmCloud01,
                          [xpos, random.randrange(0, round(FRAMEHEIGHT*TILESIZE/4))],
                          speed))

            self.mmOptions_Button = pygame.transform.scale(
                pygame.image.load(MAIN_MENU_DIRECTORY + 'Options_Button.png'),
                (50,
                 100))

    def draw_mainmenu(self):
        # draw background image
        self.WORLD.surface.blit(self.mmBackground, (0, 0))

        # draw ground floor
        self.WORLD.surface.blit(self.mmBgFloor, (0, (FRAMEHEIGHT*TILESIZE - self.mmBgFloor.get_height())))
        #pygame.draw.rect(self.WORLD.surface, (34, 139, 34),
        #                 Rect((0, ((TILESIZE * FRAMEHEIGHT) - (TILESIZE * HUDSIZE_BOTTOM))),
        #                      (TILESIZE * FRAMEWIDTH, TILESIZE * HUDSIZE_BOTTOM)))

        # draw clouds
        for c in self.mm_clouds:
            self.WORLD.surface.blit(c.surface, c.currPos)

        # draw castle
        self.WORLD.surface.blit(self.mmCastle, (0, 0))

        # draw characters
        for i in range(4):
            #self.WORLD.surface.blit(self.mmLockedCharacter_Knight, (self.charPosition[i], 450))
            self.WORLD.surface.blit(self.mm_character_loadout[i], (self.charPosition[i], 450))

        # draw buttons

        # tick
        self.tick_mainmenu()

    def tick_mainmenu(self):
        for c in self.mm_clouds:
            c.move()
            c.bounds_check()

    def release_mainmenu(self):
        del self.mmBackground
        del self.mmBackground
        del self.mmLockedCharacter_Knight
        del self.charPosition
        del self.mm_clouds
        del self.mm_character_loadout

        self.mainmenu_loaded = False

    # Handle navigation of main menu ui
    def navigate_mainmenu(self, input_direction):
        None

    def change_char(self, num):
        new_index = self.mm_character_index + num
        if new_index >= 0 and new_index < 4:
            self.mm_character_loadout[new_index] = self.mm_character_selected
            self.mm_character_loadout[self.mm_character_index] = self.mm_character_saves[self.mm_character_index].surface
            self.mm_character_index = new_index

    # Return the selected option
    def getSelection(self):
        # return either the chracter code to load a game or start new game
        # or return code to load options menu?
        return None

#######################################################################################################################
#                                    Private Helper Classes for GameEngine
#######################################################################################################################

# Cloud class used to hold information on the sprites on the main menu
class Cloud:

    def __init__(self, surface, spawn_pos, speed):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.spawnPos = copy.deepcopy(spawn_pos)
        self.currPos = spawn_pos
        self.speed = speed

    def bounds_check(self):
        if self.speed > 0:
            if self.currPos[0] > FRAMEWIDTH * TILESIZE:
                self.currPos = self.spawnPos
        elif self.speed < 0:
            if self.currPos[0] < -self.width:
                self.currPos[0] = self.spawnPos[0]

    def move(self):
        self.currPos[0] += self.speed

class GameSaves:

    def __init__(self, index, surface, savefile, newgame=True):
        self.index = index
        self.surface = surface
        self.savefile = savefile
        self.newgame = newgame

    def newGame(self):
        if self.newgame:
            # make new savefile (from newgame file template)
            None

    def loadGame(self):
        if not self.newgame:
            None

    def deleteGame(self):
        if not self.newgame:
            None

class MainMenuState:
    MAIN, EXISTING_SAVE_OPTIONS, LOAD_CONFIRM, SAVE_STATUS, DELETE_SAVE_CONFIRM, NEW_GAME_CONFIRM, OPTIONS, CREDITS = range(8)

#######################################################################################################################
#                                          Global Functions
#######################################################################################################################

# sureface, image, (x,y), alpha
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

# calculates resizing of rectangle, while keeping aspect ratio
def scale_aspect(width, height, x, y, maximum=True):
    new_width = y * width / height
    new_height = x * height / width
    if maximum ^ (new_width >= x):
        return new_width or 1, y
    return x, new_height or 1