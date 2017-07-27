from functions import *
from font_loader import *
from Controls import *

class UI:

    def __init__(self, frame_surface):
        self.frame_surface = frame_surface
        self.state = UI_State.NONE
        self.prompt_index = Confirmation_State.IDLE

        # load UI sprites
        # Alert Frame
        self.prompt_frame = pygame.transform.scale(
            pygame.image.load(imageLibrary.promptFrame),
            (int(FRAMEPIXELWIDTH * .8),
             int(FRAMEPIXELHEIGHT * 0.5)))

        button_template = pygame.image.load(imageLibrary.yesButton)
        button_ratio = scale_aspect(button_template.get_width(), button_template.get_height(), (FRAMEPIXELWIDTH * .3), 0)

        # Confirm Button
        self.yes_button = pygame.transform.scale(
            pygame.image.load(imageLibrary.yesButton),
            (int(button_ratio[0]),
             int(button_ratio[1])))
        # No Button
        self.no_button = pygame.transform.scale(
            pygame.image.load(imageLibrary.noButton),
            (int(button_ratio[0]),
             int(button_ratio[1])))
        # NewGame
        self.newgame_button = pygame.transform.scale(
            pygame.image.load(imageLibrary.newGameButton),
            (int(button_ratio[0]),
             int(button_ratio[1])))
        # Load
        self.loadgame_button = pygame.transform.scale(
            pygame.image.load(imageLibrary.loadButton),
            (int(button_ratio[0]),
             int(button_ratio[1])))
        # Delete
        self.deletegame_button = pygame.transform.scale(
            pygame.image.load(imageLibrary.deleteButton),
            (int(button_ratio[0]),
             int(button_ratio[1])))


    def loadPrompt(self, type):
        if type == UI_State.NONE:
            return

        self.state = type
        self.prompt_index = Confirmation_State.CANCEL

        # create prompt surface
        self.surface = pygame.Surface(self.prompt_frame.get_size())

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
                       int(self.prompt_frame.get_width() - (self.no_button.get_width() + (self.prompt_frame.get_width()*0.1)))]
        self.prompt_buttonY_pos = self.prompt_frame.get_height() - (self.yes_button.get_height() * 2)

    def drawPrompt(self):
        # draw text to prompt window
        for idx, line in enumerate(self.promptLines):
            currLine = textDef.font.render(line, False, (0, 0, 0))
            currPos = ((self.prompt_frame.get_width() - currLine.get_width()) // 2,
                       idx * textDef.font_size + self.promptOffsetY)
            self.surface.blit(currLine, currPos)

        # draw option buttons to prompt window
        self.surface.blit(self.yes_button, (self.prompt_buttonX_pos[0], self.prompt_buttonY_pos))
        self.surface.blit(self.no_button, (self.prompt_buttonX_pos[1], self.prompt_buttonY_pos))

        # draw the selected option
        # self.prompt_index

        # draw prompt window to frame (10% width padding, and 40% from the top)
        self.frame_surface.blit(self.surface, (int(FRAMEPIXELWIDTH * 0.1), int(FRAMEPIXELHEIGHT * 0.4)))

    def handleEvent(self, event):
        if event.key == C_SELECT:
            return self.prompt_index
        elif event.key == C_LEFT:
            self.prompt_index = Confirmation_State.CONFIRM
        elif event.key == C_RIGHT:
            self.prompt_index = Confirmation_State.CANCEL

        return Confirmation_State.IDLE

class UI_State:
    NONE, NEWGAME, DELETE, LOAD  = range(4)

class Confirmation_State:
    IDLE, CONFIRM, CANCEL = range(3)