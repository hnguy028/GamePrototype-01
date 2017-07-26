from functions import *
from GameClasses import *
from gameEngine import *
from Loot_2D import *

pygame.init()

# Clock cycle
mainClock = pygame.time.Clock()

# Game state
state = State.START_MENU
running = True

# Instantiate game loader
l = gameEngine()
l.loadSurface()


# Game loop
while running:
    # game_state
    if state == State.GAME:
        if not l.gameLoaded:
            l.loadGame()
            WORLD = l.WORLD
            ROOM = l.ROOM
            PLAYER = l.PLAYER
            HUD = l.HUD
            COIN = Coin1()

        # draw current room to screen
        ROOM.drawMap(WORLD.surface)

        COIN.getCoin(ROOM)
        COIN.drawCoin(WORLD.surface)
        COIN.removeCoin(PLAYER.x + PLAYER.width/2, PLAYER.y + PLAYER.height/2)

        for event in pygame.event.get():  # event handling loop

            # handle exit button press
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_p:
                    state = State.START_MENU

                PLAYER.handleKeyDown(event)

            elif event.type == KEYUP:
                PLAYER.handleKeyUp(event)

        if PLAYER.moveUp or PLAYER.moveDown or PLAYER.moveLeft or PLAYER.moveRight:
            # if in motion, then draw animation
            PLAYER.walkRunMotion(WORLD)

            curRate = 0

            if PLAYER.running:
                curRate = PLAYER.runRate
            else:
                curRate = PLAYER.walkRate

            if PLAYER.moveUp:
                PLAYER.move_Up(curRate, TILESIZE, ROOM)
            if PLAYER.moveDown:
                PLAYER.move_Down(curRate, TILESIZE, ROOM)
            if PLAYER.moveLeft:
                PLAYER.move_Left(curRate, TILESIZE, ROOM)
            if PLAYER.moveRight:
                PLAYER.move_Right(curRate, TILESIZE, ROOM)

        else:
            PLAYER.idle(WORLD)

        # make sure the player does move off the screen
        PLAYER.boundsCheck(ROOM)

        # check if the player has stepped into a portal object
        checkPortal(PLAYER, ROOM, WORLD)

        #       coinx, coiny, coinq = getCoin()
        #        world.loadMap()

        # TODO : add gui
        HUD.drawRect(WORLD.surface)
        # create menu gui - player menu / controls
        # windowSurface.blit(instructionSurf, instructionRect)
    elif state == State.START_MENU:
        # Check if main menu is already loaded
        if not l.mainMenuLoaded:
            l.load_mainmenu()

        # Draw main menu
        l.draw_mainmenu()

        # event handling loop
        for event in pygame.event.get():

            # handle exit button press
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RETURN:
                    state = State.GAME
                elif event.key == K_LEFT:
                    l.change_char(-1)
                elif event.key == K_RIGHT:
                    l.change_char(1)
            #elif event.type == KEYUP:
                #PLAYER.handleKeyUp(event)
    else:
        print("State Error")
        pygame.quit()
        sys.exit()
    # END if statement

    # Update display
    pygame.display.update()
    mainClock.tick(30)  # fps / clock speed

    # END WHILE LOOP

# Add desctructor
l.releaseMainMenu()
