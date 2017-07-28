from functions import *
from resource_loader import *
from Controls import *

class UI:

    def __init__(self, frame_surface):
        self.frame_surface = frame_surface
        self.state = UI_State.NONE
        self.prompt_index = Confirmation_State.IDLE

        # frame variables
        self.frameWidth = int(FRAMEPIXELWIDTH * .9)
        self.frameHorizontalPadding = (FRAMEPIXELWIDTH - self.frameWidth) // 2
        self.frameHeight = int(FRAMEPIXELHEIGHT * 0.5)

        # load UI sprites
        # Alert Frame
        self.prompt_frame = imageLibrary.load(imageDirectory.promptFrame,
                                              self.frameWidth,
                                              self.frameHeight)

        button_template = pygame.image.load(imageDirectory.yesButton)
        button_ratio = scale_aspect(button_template.get_width(), button_template.get_height(), (FRAMEPIXELWIDTH * .3), 50)

        # Confirm Button
        self.yes_button = imageLibrary.load(imageDirectory.yesButton,
                                                   int(button_ratio[0]),
                                                   int(button_ratio[1]))
        # No Button
        self.no_button = imageLibrary.load(imageDirectory.noButton,
                                                   int(button_ratio[0]),
                                                   int(button_ratio[1]))
        # NewGame
        self.newgame_button = imageLibrary.load(imageDirectory.newGameButton,
                                                   int(button_ratio[0]),
                                                   int(button_ratio[1]))
        # Load
        self.loadgame_button = imageLibrary.load(imageDirectory.loadButton,
                                                   int(button_ratio[0]),
                                                   int(button_ratio[1]))
        # Delete
        self.deletegame_button = imageLibrary.load(imageDirectory.deleteButton,
                                                   int(button_ratio[0]),
                                                   int(button_ratio[1]))
        # Delete
        self.selector_image = imageLibrary.load(imageDirectory.selectHover,
                                                   int(button_ratio[0]),
                                                   int(button_ratio[1]))

        #self.deletegame_button = pygame.transform.scale(
         #   pygame.image.load(imageDirectory.deleteButton),
          #  (int(button_ratio[0]),
           #  int(button_ratio[1])))


    def loadPrompt(self, type):
        if type == UI_State.NONE:
            return

        self.state = type
        self.prompt_index = Confirmation_State.CANCEL

        # create prompt surface
        self.promptSurface = pygame.Surface(self.prompt_frame.get_size())
        self.promptSurface.fill((150,50,50,0))
        self.promptSurface.set_alpha(int(MAX_ALPHA * .9))

        # load image defined by type
        if type == UI_State.NEWGAME:
            prompt_msg = "Create a New Game?"
        elif type == UI_State.LOAD:
            prompt_msg = "Load Game?"
        elif type == UI_State.DELETE:
            prompt_msg = "Delete Game?"

        # parse prompt msg
        self.promptLines = prompt_msg.splitlines()
        self.promptOffsetY = (self.prompt_frame.get_height() - len(self.promptLines) * (textDef.font_size + 1)) // 4
        self.prompt_buttonX_pos = [int(self.prompt_frame.get_width()*0.1),
                       self.prompt_frame.get_width() - self.no_button.get_width() - int(self.prompt_frame.get_width()*0.1)]
        self.prompt_buttonY_pos = self.prompt_frame.get_height() - (self.yes_button.get_height())

    def drawPrompt(self):
        # draw frame background image
        self.promptSurface.fill((150, 50, 50))
        # self.promptSurface.blit(self.prompt_frame, (0,0))

        # draw text to prompt window
        for idx, line in enumerate(self.promptLines):
            currLine = textDef.font.render(line, False, (0, 0, 0))
            currPos = ((self.prompt_frame.get_width() - currLine.get_width()) // 2,
                       idx * textDef.font_size + self.promptOffsetY)
            self.promptSurface.blit(currLine, currPos)

        # draw option buttons to prompt window
        self.promptSurface.blit(self.yes_button, (self.prompt_buttonX_pos[0], self.prompt_buttonY_pos))
        self.promptSurface.blit(self.no_button, (self.prompt_buttonX_pos[1], self.prompt_buttonY_pos))

        # draw the selected option
        if self.prompt_index == Confirmation_State.CONFIRM:
            self.promptSurface.blit(self.selector_image, (self.prompt_buttonX_pos[0], self.prompt_buttonY_pos))
        elif self.prompt_index == Confirmation_State.CANCEL:
            self.promptSurface.blit(self.selector_image, (self.prompt_buttonX_pos[1], self.prompt_buttonY_pos))

        # draw prompt window to frame (10% width padding, and 40% from the top)
        self.frame_surface.blit(self.promptSurface, (self.frameHorizontalPadding, int(FRAMEPIXELHEIGHT * 0.4)))

    def loadOptions(self):
        self.optionSurface = pygame.Surface((int(FRAMEPIXELWIDTH * .95), int(FRAMEPIXELHEIGHT * .95)))
        self.optionSurface.fill((230, 230, 230, 0))
        self.optionSurface.set_alpha(int(MAX_ALPHA * .9))

    def drawOptions(self):
        # in this case vertical padding = horizontal padding (which should be 5% of the frame)
        self.frame_surface.blit(self.optionSurface, (self.frameHorizontalPadding // 2, self.frameHorizontalPadding // 2))

    def handleEvent(self, event):
        if event.key == C_SELECT:
            return self.prompt_index
        elif event.key == C_LEFT:
            self.prompt_index = Confirmation_State.CONFIRM
        elif event.key == C_RIGHT:
            self.prompt_index = Confirmation_State.CANCEL

        return Confirmation_State.IDLE


class MainMenuState:
    # Other state means we are not in the main menu
    MAIN, EXISTING_SAVE_OPTIONS, UI_PROMPT, SAVE_STATUS, OPTIONS, CREDITS, OTHER = range(7)

# State to determine which confirmation prompt to display
class UI_State:
    NONE, NEWGAME, DELETE, LOAD  = range(4)

# return values of coonfirmation prompts
class Confirmation_State:
    IDLE, CONFIRM, CANCEL = range(3)