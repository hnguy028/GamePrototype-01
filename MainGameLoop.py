from gameEngine import *
from Loot_2D import *

# Clock cycle
mainClock = pygame.time.Clock()

# Game status
running = True

# Instantiate game loader
l = gameEngine()
l.loadSurface()


# Game loop
while running:
    # game_state
    if l.state == State.GAME:
        if not l.gameLoaded:
            l.loadGame()


        for event in pygame.event.get():  # event handling loop

            # handle exit button press
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                l.handleGameEvent(event)

        l.drawGame()


    elif l.state == State.START_MENU:
        # load main menu
        l.load_mainmenu()

        # draw main menu
        l.draw_mainmenu()

        # event handling loop
        for event in pygame.event.get():

            # handle exit button press
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                l.handleEvent(event)
    else:
        print("State Error")
        pygame.quit()
        sys.exit()
    # END if statement

    # Update display
    pygame.display.update()
    mainClock.tick(FPS)  # fps / clock speed

    # END WHILE LOOP

# Add desctructor
l.releaseMainMenu()

pygame.quit()
sys.exit()