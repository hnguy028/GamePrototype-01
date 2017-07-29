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

        # MainMenuUI Variables
        # dictionary conatining lists of sprites to be drawn
        self.mm_ui_list = {}
        # indices used to keep track of selected option
        self.mm_ui_keyIndex = 0
        self.mm_ui_listIndex = 0

        self.mm_clouds = []
        self.mm_game_saves = []
        self.mm_selection = Selection.CHARACTER00

    def handleEvent(self, event):

        if self.state == MainMenuState.MAIN:

            if event.key == C_SELECT:
                print(self.mm_selection)
                if self.mm_selection <= Selection.CHARACTER03:
                    # newgame, load options
                    None
                elif self.mm_selection == Selection.CONTROL_SETTINGS:
                    self.state = MainMenuState.CONTROLS
                    self.ui.loadControlSettings()
                elif self.mm_selection == Selection.OPTIONS:
                    self.state = MainMenuState.OPTIONS
                    self.ui.loadOptions()
                elif self.mm_selection == Selection.CREDITS:
                    # roll credits
                    self.state = MainMenuState.CREDITS
                    self.mm_music.stop()
                    self.credit_music = audioLibrary.load(audioDirectory.mainmenu_music)
                    self.credit_music.play()

            elif event.key in [C_UP, C_DOWN, C_LEFT, C_RIGHT]:
                self.update_selection(event)

        elif self.state == MainMenuState.UI_PROMPT:
            res = self.ui.handleEvent(event, self.state)
            if res == Confirmation_State.CONFIRM:
                self.state = MainMenuState.OTHER
                self.ui.state = UI_State.NONE

            elif res == Confirmation_State.CANCEL:
                self.state = MainMenuState.MAIN
                self.ui.state = UI_State.NONE

        elif self.state == MainMenuState.CONTROLS:
            if event.key == C_SELECT:
                self.state = MainMenuState.MAIN

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
            self.mmCastle = Sprite(
                imageLibrary.load(imageDirectory.mainmenu_castle, FRAMEPIXELWIDTH, int(FRAMEPIXELHEIGHT * 0.9)))

            # Main Menu Background Image
            self.mmBackground = Sprite(
                imageLibrary.load(imageDirectory.mainmenu_background, FRAMEPIXELWIDTH, FRAMEPIXELHEIGHT - int(FRAMEPIXELHEIGHT * 0.2)))

            # Background Floor Image
            self.mmBgFloor = Sprite(
                imageLibrary.load(imageDirectory.mainmenu_floor, FRAMEPIXELWIDTH, int(FRAMEPIXELHEIGHT * 0.5)),
                (0, (FRAMEPIXELHEIGHT - int(FRAMEPIXELHEIGHT * 0.5))))

            # Locked Character Image
            self.mmLockedCharacter_Knight = pygame.transform.scale(
                pygame.image.load(imageDirectory.lockedCharacter),
                (50, 100))

            for i in range(4):
                self.mm_game_saves.append(GameSaves(i, self.mmLockedCharacter_Knight, SAVE_DIRECTORY + 'savefile_0' + str(i)))

            self.mm_character_selected = pygame.transform.scale(
                pygame.image.load(imageDirectory.knight),
                (50, 100))

            # Load Character from file if it exists
            for i in range(4):
                try:
                    savefile = open(SAVE_DIRECTORY + 'savefile_0' + str(i), 'r')
                    char_name = savefile.readline()

                    loaded_character = pygame.transform.scale(
                        pygame.image.load(MAIN_MENU_DIRECTORY + char_name),
                        (50, 100))

                    self.mm_game_saves[i] = GameSaves(i, loaded_character, SAVE_DIRECTORY + 'savefile_0' + str(i), False)

                    savefile.close()
                except Exception:
                    None # Do Nothing

            # calculate the equal distance between each character position
            char_margin = FRAMEPIXELWIDTH / 8
            posCorrection = self.mmLockedCharacter_Knight.get_width() / 2
            charXPosition = [char_margin - posCorrection,
                            (char_margin*3) - posCorrection,
                            (char_margin*5) - posCorrection,
                            (char_margin*7) - posCorrection]
            charYPosition = 450

            # set character 00 as default selected
            self.mm_ui_list["0"] = [Sprite(self.mm_character_selected, (charXPosition[0], charYPosition))]
            # load the rest of the chracters into ui list
            for i in range(1,4):
                self.mm_ui_list["0"].append(Sprite(self.mm_game_saves[i].surface,(charXPosition[i], charYPosition)))

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

                xpos = random.randrange(mmCloudWidth, mmCloudWidth*3)

                if speed < 0:
                    xpos += (FRAMEWIDTH * TILESIZE)
                else:
                    xpos = -xpos

                # add the cloud to list of clouds to be drawn
                self.mm_clouds.append(
                    Cloud(self.mmCloud01,
                          [xpos, random.randrange(0, int(FRAMEPIXELHEIGHT/4))],
                          speed))

            button_template = imageLibrary.load(imageDirectory.blankButton, 100, 100, True)
            button_ratio = [button_template.get_width(), button_template.get_height()]

            # Controls Settings Button
            self.controls_button = imageLibrary.load(imageDirectory.controlSettingsButton,
                                                    button_ratio[0], button_ratio[1])

            # Options Button
            self.options_button = imageLibrary.load(imageDirectory.optionsButton,
                                                    button_ratio[0], button_ratio[1])

            # Credits Button
            self.credits_button = imageLibrary.load(imageDirectory.creditsButton,
                                                    button_ratio[0], button_ratio[1])

            # Add Buttons to user interface list
            # char pos, char height, padding
            buttonPosY = charYPosition + self.mmLockedCharacter_Knight.get_height() + 10
            buttonPosX = button_template.get_width() + 10

            self.mm_ui_list["1"] = []
            self.mm_ui_list["1"].append(Sprite(self.controls_button, (FRAMEPIXELWIDTH - buttonPosX * 3, buttonPosY)))
            self.mm_ui_list["1"].append(Sprite(self.options_button, (FRAMEPIXELWIDTH - buttonPosX * 2, buttonPosY)))
            self.mm_ui_list["1"].append(Sprite(self.credits_button, (FRAMEPIXELWIDTH - buttonPosX, buttonPosY)))


            # Load and play bg music
            self.mm_music = audioLibrary.load(audioDirectory.mainmenu_music)
            self.mm_music.play(-1)

    def draw_mainmenu(self):
        if self.state <= MainMenuState.UI_PROMPT:
            # draw background image
            self.mmBackground.draw(self.WORLD.surface)

            # draw ground floor
            self.mmBgFloor.draw(self.WORLD.surface)

            # draw clouds
            for c in self.mm_clouds:
                self.WORLD.surface.blit(c.surface, c.currPos)

            # draw castle
            self.mmCastle.draw(self.WORLD.surface)

            # load cursor position to the selected option
            selected_sprite = self.mm_ui_list[str(self.mm_ui_keyIndex)][self.mm_ui_listIndex]
            cursor_x = selected_sprite.pos[0] + selected_sprite.image.get_width() // 2
            cursor_y = selected_sprite.pos[1] + selected_sprite.image.get_height() // 2
            self.mm_ui_list["-1"] = [Sprite(self.ui.cursor, (cursor_x, cursor_y))]

            # draw user interface
            for key in self.mm_ui_list:
                for sprite in self.mm_ui_list[key]:
                    self.WORLD.surface.blit(sprite.image, sprite.pos)

            # draw prompt
            if self.state == MainMenuState.UI_PROMPT:
                self.ui.drawPrompt()

            # tick
            self.tick_mainmenu()
        elif self.state == MainMenuState.CONTROLS:
            self.ui.drawControlSettings()
        elif self.state == MainMenuState.OPTIONS:
            self.ui.drawOptions()
        elif self.state == MainMenuState.CREDITS:
            self.WORLD.surface.fill((0, 0, 0, 0))

    def tick_mainmenu(self):
        for c in self.mm_clouds:
            c.move()
            c.bounds_check()

    # Handle navigation of main menu ui
    def update_selection(self, event):
        if event.key == C_UP:
            self.mm_ui_keyIndex = max(0, self.mm_ui_keyIndex - 1)
        elif event.key == C_DOWN:
            self.mm_ui_keyIndex = min(1, self.mm_ui_keyIndex + 1)
            self.mm_ui_listIndex = min(self.mm_ui_listIndex, len(self.mm_ui_list[str(self.mm_ui_keyIndex)])-1)
        elif event.key == C_LEFT:
            self.mm_ui_listIndex = max(0, self.mm_ui_listIndex - 1)
        elif event.key == C_RIGHT:
            self.mm_ui_listIndex = min(len(self.mm_ui_list[str(self.mm_ui_keyIndex)]) - 1, self.mm_ui_listIndex + 1)

        selection_offset = 0 if self.mm_ui_keyIndex == 0 else 4
        self.mm_selection = selection_offset + self.mm_ui_listIndex

    # Should only be called when moving to game load state
    def release_mainmenu(self):
        del self.mmBackground
        del self.mmLockedCharacter_Knight
        del self.mm_clouds
        del self.mm_character_loadout
        del self.mm_music

        self.mainmenu_loaded = False

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