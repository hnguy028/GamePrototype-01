from GameClasses import *
from UI import *
import copy

class gameEngine:

    def __init__(self):
        # Init main menu variables
        self.state = None
        self.frameLoaded = False
        self.mainMenuLoaded = False
        self.gameLoaded = False

        self.mm_clouds = []
        self.mm_character_loadout = []
        self.mm_character_saves = []
        self.mm_character_selected = None
        self.mm_selection = Selection.CHARACTER00

    def handleEvent(self, event):

        if self.state == MainMenuState.MAIN:

            if event.key == C_SELECT:

                if self.mm_selection <= Selection.CHARACTER03:
                    # newgame, load options
                    None
                elif self.mm_selection == Selection.CONTROL_SETTINGS:
                    None
                elif self.mm_selection == Selection.OPTIONS:
                    None
                elif self.mm_selection == Selection.CREDITS:
                    # roll credits
                    self.state = MainMenuState.CREDITS
                    self.mm_music.stop()
                    self.credit_music = audioLibrary.load(audioDirectory.mainmenu_music)
                    self.credit_music.play()

            elif event.key == C_UP:
                self.update_selection(-4)

            elif event.key == C_DOWN:
                self.update_selection(4)

            elif event.key == C_LEFT:
                self.update_selection(-1)

            elif event.key == C_RIGHT:
                self.update_selection(1)

            elif event.key == K_HOME:
                self.state = MainMenuState.UI_PROMPT
                self.ui.loadPrompt(UI_State.NEWGAME)

            elif event.key == K_DELETE:
                self.state = MainMenuState.OPTIONS
                self.ui.loadOptions()

        elif self.state == MainMenuState.UI_PROMPT:
            res = self.ui.handleEvent(event)
            if res == Confirmation_State.CONFIRM:
                self.state = MainMenuState.OTHER
                self.ui.state = UI_State.NONE

            elif res == Confirmation_State.CANCEL:
                self.state = MainMenuState.MAIN
                self.ui.state = UI_State.NONE

        elif self.state == MainMenuState.OPTIONS:
            if event.key == C_SELECT:
                self.state = MainMenuState.MAIN

        elif self.state == MainMenuState.CREDITS:
            if event.type == KEYDOWN:
                self.state = MainMenuState.MAIN

        # if state is set to other then we can break out of the main menu states
        return self.state == MainMenuState.OTHER

    def loadSurface(self):
        if not self.frameLoaded:
            self.frameLoaded = True
            self.WORLD = WindowSurface(HUDSIZE_BOTTOM, ROOMWIDTH, ROOMHEIGHT)
            self.ui = UI(self.WORLD.surface)
            self.state = MainMenuState.MAIN

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
                pygame.image.load(imageDirectory.mainmenu_castle),
                    (FRAMEPIXELWIDTH,
                     FRAMEPIXELHEIGHT - int(FRAMEPIXELHEIGHT * 0.1)))

            # Main Menu Background Image
            self.mmBackground = pygame.transform.scale(
                pygame.image.load(imageDirectory.mainmenu_background),
                    (FRAMEPIXELWIDTH,
                     FRAMEPIXELHEIGHT - int(FRAMEPIXELHEIGHT * 0.2)))

            # Background Floor Image
            self.mmBgFloor = pygame.transform.scale(
                pygame.image.load(imageDirectory.mainmenu_floor),
                    (FRAMEPIXELWIDTH,
                     FRAMEPIXELHEIGHT - int(FRAMEPIXELHEIGHT * 0.5)))

            # Locked Character Image
            self.mmLockedCharacter_Knight = pygame.transform.scale(
                pygame.image.load(imageDirectory.lockedCharacter),
                (50, 100))

            for i in range(4):
                self.mm_character_loadout.append(self.mmLockedCharacter_Knight)
                self.mm_character_saves.append(GameSaves(i, self.mmLockedCharacter_Knight, ""))

            self.mm_character_selected = pygame.transform.scale(
                pygame.image.load(imageDirectory.knight),
                (50, 100))

            self.mm_character_loadout[0] = self.mm_character_selected

            # Load Character from file if it exists
            for i in range(4):
                try:
                    savefile = open(SAVE_DIRECTORY + 'savefile_0' + str(i), 'r')
                    char_name = savefile.readline()

                    loaded_character = pygame.transform.scale(
                        pygame.image.load(MAIN_MENU_DIRECTORY + char_name),
                        (50, 100))

                    self.mm_character_saves[i] = GameSaves(i, loaded_character, SAVE_DIRECTORY + 'savefile_0' + str(i), False)

                    savefile.close()
                except Exception:
                    None # Do nothing

            # calculate the equal distance between each character position
            char_margin = FRAMEPIXELWIDTH / 8
            posCorrection = self.mmLockedCharacter_Knight.get_width() / 2
            self.charPosition = [char_margin - posCorrection,
                                 (char_margin*3) - posCorrection,
                                 (char_margin*5) - posCorrection,
                                 (char_margin*7) - posCorrection]

            # load cloud images (cant use imageLibrary)
            loaded_cloud = pygame.image.load(MAIN_MENU_DIRECTORY + "cloud.png")

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
                          [xpos, random.randrange(0, int(FRAMEPIXELHEIGHT/4))],
                          speed))

            button_template = imageLibrary.load(imageDirectory.creditsButton)
            button_ratio = scale_aspect(button_template.get_width(), button_template.get_height(),
                                        (FRAMEPIXELWIDTH * .3), 50)

            # Controls Settings Button
            #self.options_button = imageLibrary.load(imageDirectory.optionsButton,
            #                                        int(button_ratio[0]),
            #                                        int(button_ratio[1]))

            # Options Button
            self.options_button = imageLibrary.load(imageDirectory.optionsButton,
                                                int(button_ratio[0]),
                                                int(button_ratio[1]))

            # Credits Button
            self.credits_button = imageLibrary.load(imageDirectory.creditsButton,
                                                    int(button_ratio[0]),
                                                    int(button_ratio[1]))

            self.mm_music = audioLibrary.load(audioDirectory.mainmenu_music)
            self.mm_music.play(-1)

    def draw_mainmenu(self):
        if self.state < MainMenuState.CREDITS:
            # draw background image
            self.WORLD.surface.blit(self.mmBackground, (0, 0))

            # draw ground floor
            self.WORLD.surface.blit(self.mmBgFloor, (0, (FRAMEPIXELHEIGHT - self.mmBgFloor.get_height())))
            #pygame.draw.rect(self.WORLD.surface, (34, 139, 34),
            #                 Rect((0, ((TILESIZE * FRAMEHEIGHT) - (TILESIZE * HUDSIZE_BOTTOM))),
            #                      (FRAMEPIXELWIDTH, TILESIZE * HUDSIZE_BOTTOM)))

            # draw clouds
            for c in self.mm_clouds:
                self.WORLD.surface.blit(c.surface, c.currPos)

            # draw castle
            self.WORLD.surface.blit(self.mmCastle, (0, 0))

            # draw characters
            for i in range(4):
                #self.WORLD.surface.blit(self.mmLockedCharacter_Knight, (self.charPosition[i], 450))
                self.WORLD.surface.blit(self.mm_character_loadout[i], (self.charPosition[i], 450))

            # draw controls, options, and credit buttons


            # draw prompt
            if self.state == MainMenuState.UI_PROMPT:
                self.ui.drawPrompt()
            elif self.state == MainMenuState.OPTIONS:
                self.ui.drawOptions()

            # tick
            self.tick_mainmenu()
        elif self.state == MainMenuState.CREDITS:
            self.WORLD.surface.fill((50, 250, 50, 0))

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
    def update_selection(self, step):
        if step > 0:
            new_index = min(self.mm_selection + step,7)
        else:
            new_index = max(self.mm_selection + step, 0)

        if new_index in range(4) and self.mm_selection in range(4):
            self.mm_character_loadout[new_index] = self.mm_character_selected
            self.mm_character_loadout[self.mm_selection] = self.mm_character_saves[self.mm_selection].surface
            self.mm_selection = new_index

        if 0 <= Selection.CHARACTER03:
           None



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
            if self.currPos[0] > FRAMEPIXELWIDTH:
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

class Selection:
    CHARACTER00, CHARACTER01, CHARACTER02, CHARACTER03, CONTROL_SETTINGS, OPTIONS, CREDITS = range(7)