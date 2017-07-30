from GameClasses import *
from UI import *
## TODO remove
from Loot_2D import *
import copy

class gameEngine:

    def __init__(self):
        # Init gameEngine Variables

        # gameEngine state
        self.state = State.START_MENU
        self.mainMenuState = None

        # Handelers on which resources are loaded
        self.frameLoaded = False
        self.mainMenuLoaded = False
        self.gameLoaded = False

        self.game_saves = []

    def handleEvent(self, event):
        if self.state == State.INITIAL_LOAD:
            None
        elif self.state == State.START_MENU:
            if self.handleMainMenuEvent(event):
                self.state = State.GAME
        elif self.state == State.GAME:
            if event.key == C_DELETE:
                # NOT being accessed for some reason
                self.state = State.START_MENU
            self.handleGameEvent(event)

    def handleMainMenuEvent(self, event):

        # if main menu or confirmation prompt
        if self.mainMenuState <= MainMenuState.UI_PROMPT:

            if self.mainMenuState == MainMenuState.MAIN:

                if event.key == C_SELECT:
                    if self.mm_selection <= Selection.CHARACTER03:
                        character_index = self.mm_selection
                        # check if the character selected has a stored save
                        if not self.game_saves[character_index].newgame:
                            self.ui.loadPrompt(UI_State.LOAD)
                            self.mainMenuState = MainMenuState.UI_PROMPT
                        else:
                            self.ui.loadPrompt(UI_State.NEWGAME)
                            self.mainMenuState = MainMenuState.UI_PROMPT

                    elif self.mm_selection == Selection.CONTROL_SETTINGS:
                        self.mainMenuState = MainMenuState.CONTROLS
                        self.ui.loadControlSettings()
                    elif self.mm_selection == Selection.OPTIONS:
                        self.mainMenuState = MainMenuState.OPTIONS
                        self.ui.loadOptions()
                    elif self.mm_selection == Selection.CREDITS:
                        # roll credits
                        self.mainMenuState = MainMenuState.CREDITS
                        self.mm_music.stop()
                        self.credit_music = audioLibrary.load(audioDirectory.credit_music)
                        self.credit_music.play()

                # navigate the main menu options
                elif event.key in [C_UP, C_DOWN, C_LEFT, C_RIGHT]:
                    self.update_selection(event)

                # character deletion
                elif self.mm_selection <= Selection.CHARACTER03 and event.key == C_DELETE:
                    character_index = self.mm_selection

                    # if game save exists
                    if not self.game_saves[character_index].newgame:
                        self.ui.loadPrompt(UI_State.DELETE)
                        self.mainMenuState = MainMenuState.UI_PROMPT

            # UI_PROMOPT State
            else:
                # get prompt confirmation
                confirmation = self.ui.handleEvent(event)

                if confirmation == Confirmation_State.CONFIRM:

                    if self.ui.state == UI_State.LOAD:
                        self.mainMenuState = MainMenuState.OTHER
                        self.ui.state = UI_State.NONE
                        self.mm_music.stop()

                    elif self.ui.state == UI_State.NEWGAME:
                        #self.mainMenuState = MainMenuState.OTHER
                        self.ui.state = UI_State.NONE

                    elif self.ui.state == UI_State.DELETE:
                        #self.mainMenuState = MainMenuState.OTHER
                        self.ui.state = UI_State.NONE

                elif confirmation == Confirmation_State.CANCEL:
                    self.mainMenuState = MainMenuState.MAIN
                    self.ui.state = UI_State.NONE

        elif self.mainMenuState == MainMenuState.CONTROLS:
            if event.key == C_SELECT:
                self.mainMenuState = MainMenuState.MAIN

        elif self.mainMenuState == MainMenuState.OPTIONS:
            if event.key == C_SELECT:
                self.mainMenuState = MainMenuState.MAIN

        elif self.mainMenuState == MainMenuState.CREDITS:
            if event.type == KEYDOWN:
                self.mainMenuState = MainMenuState.MAIN
                self.credit_music.stop()
                self.mm_music.play(-1)

        # if state is set to other then we can break out of the main menu states
        return self.mainMenuState == MainMenuState.OTHER

    def handleGameEvent(self, event):

        if event.type == KEYDOWN:
            self.PLAYER.handleKeyDown(event)
        elif event.type == KEYUP:
            self.PLAYER.handleKeyUp(event)

        #self.drawGame()

    # loads window frame
    def loadSurface(self):
        if not self.frameLoaded:
            self.frameLoaded = True
            self.WORLD = WindowSurface(HUDSIZE_BOTTOM, ROOMWIDTH, ROOMHEIGHT)
            self.ui = UI(self.WORLD.surface)
            self.mainMenuState = MainMenuState.MAIN

    # Load Game State classes
    def loadGame(self):
        if not self.gameLoaded:
            self.gameLoaded = True
            self.ROOM = RoomSurface("desert_world2")
            self.PLAYER = Player(self.ROOM, self.ROOM.playerSpawn, CHARACTER_NAME, 100, 100, 100, DOWN)
            self.HUD = HUD()

            self.ROOM.loadMap()

            # TODO : relocate coin1
            self.COIN = Coin1()

    def drawGame(self):
        # draw current room to screen
        self.ROOM.drawMap(self.WORLD.surface)

        self.COIN.getCoin(self.ROOM)
        self.COIN.drawCoin(self.WORLD.surface)
        self.COIN.removeCoin(self.PLAYER.x + self.PLAYER.width/2, self.PLAYER.y + self.PLAYER.height/2)

        if self.PLAYER.moveUp or self.PLAYER.moveDown or self.PLAYER.moveLeft or self.PLAYER.moveRight:

            # if in motion, then draw animation
            self.PLAYER.walkRunMotion(self.WORLD)

            currRate = 0

            if self.PLAYER.running:
                currRate = self.PLAYER.runRate
            else:
                currRate = self.PLAYER.walkRate

            if self.PLAYER.moveUp:
                self.PLAYER.move_Up(currRate, TILESIZE, self.ROOM)
            if self.PLAYER.moveDown:
                self.PLAYER.move_Down(currRate, TILESIZE, self.ROOM)
            if self.PLAYER.moveLeft:
                self.PLAYER.move_Left(currRate, TILESIZE, self.ROOM)
            if self.PLAYER.moveRight:
                self.PLAYER.move_Right(currRate, TILESIZE, self.ROOM)

        else:
            self.PLAYER.idle(self.WORLD)

        # make sure the player does move off the screen
        self.PLAYER.boundsCheck(self.ROOM)

        # check if the player has stepped into a portal object
        checkPortal(self.PLAYER, self.ROOM, self.WORLD)

        #       coinx, coiny, coinq = getCoin()
        #        world.loadMap()

        # TODO : add gui
        self.HUD.drawRect(self.WORLD.surface)
        # create menu gui - player menu / controls
        # windowSurface.blit(instructionSurf, instructionRect)

    # load main menu state classes and images
    def load_mainmenu(self):
        if not self.mainMenuLoaded:
            # MainMenuUI Variables

            # dictionary conatining lists of sprites to be drawn
            self.mm_ui_list = {}
            # indices used to keep track of selected option
            self.mm_ui_keyIndex = 0
            self.mm_ui_listIndex = 0

            self.mm_clouds = []
            self.mm_selection = Selection.CHARACTER00

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
                self.game_saves.append(GameSaves(i, self.mmLockedCharacter_Knight, SAVE_DIRECTORY + 'savefile_0' + str(i)))

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

                    self.game_saves[i] = GameSaves(i, loaded_character, SAVE_DIRECTORY + 'savefile_0' + str(i), False)

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
                self.mm_ui_list["0"].append(Sprite(self.game_saves[i].surface,(charXPosition[i], charYPosition)))

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
        if self.mainMenuState <= MainMenuState.UI_PROMPT:
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

            # remove cursor if prompt is displayed
            if self.mainMenuState == MainMenuState.UI_PROMPT:
                self.mm_ui_list["-1"] = []

            # draw user interface
            for key in self.mm_ui_list:
                for sprite in self.mm_ui_list[key]:
                    self.WORLD.surface.blit(sprite.image, sprite.pos)

            # draw prompt
            if self.mainMenuState == MainMenuState.UI_PROMPT:
                self.ui.drawPrompt()

            # tick
            self.tick_mainmenu()
        elif self.mainMenuState == MainMenuState.CONTROLS:
            self.ui.drawControlSettings()
        elif self.mainMenuState == MainMenuState.OPTIONS:
            self.ui.drawOptions()
        elif self.mainMenuState == MainMenuState.CREDITS:
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

# Game State enum
class State:
    INITIAL_LOAD, START_MENU, GAME = range(3)

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