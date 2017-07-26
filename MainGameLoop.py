from functions import *
from GameClasses import *
from Loot_2D import *

pygame.init()

# Init Program
#TILESIZE = 32
#ROOMWIDTH = 15
#ROOMHEIGHT = 15

# Clock cycle
mainClock = pygame.time.Clock()

# Debugging
WORLD = WindowSurface(4*32, ROOMWIDTH, ROOMHEIGHT, "desert_world2")
ROOM = RoomSurface("desert_world2")
PLAYER = Player(ROOM, ROOM.playerSpawn, CHARACTER_NAME, 100, 100, 100, DOWN)
HUD = HUD()
COIN = Coin1()
ROOM.loadMap()

cloud = pygame.image.load('resources/menu_sprites/cloud02.png')
cloud1 = pygame.transform.scale(cloud, (270,170)) # 544 : 350
cloud1.set_alpha(128)
cloud2 = pygame.transform.flip(cloud1,True,False)
c1p = -50
c2p = 50+(TILESIZE*FRAMEWIDTH)

# Game state
state = State.START_MENU
running = True

# Game loop
while running:
    # game_state
    if state == State.GAME:
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

        pygame.display.set_icon(pygame.image.load(GAME_ICON))

        for event in pygame.event.get():  # event handling loop

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
            #elif event.type == KEYUP:
                #PLAYER.handleKeyUp(event)
        image = pygame.image.load('resources/menu_sprites/castle.png')
        image = pygame.transform.scale(image, (TILESIZE*FRAMEWIDTH, TILESIZE*(FRAMEHEIGHT-2)))

        # Sky Color
        skyimage = pygame.image.load('resources/menu_sprites/cloud_scenery.jpg')
        skyimage = pygame.transform.scale(skyimage, (TILESIZE * FRAMEWIDTH, TILESIZE * (FRAMEHEIGHT - 4)))
        WORLD.surface.blit(skyimage, (0,0))
        #pygame.draw.rect(WORLD.surface, (0, 200, 255),
                         #Rect((0, 0), (TILESIZE * FRAMEWIDTH, TILESIZE * FRAMEHEIGHT)))
        # Grass
        pygame.draw.rect(WORLD.surface, (34,139,34),
                         Rect((0, ((TILESIZE*FRAMEHEIGHT)-(TILESIZE * HUDSIZE_BOTTOM))), (TILESIZE * FRAMEWIDTH, TILESIZE * HUDSIZE_BOTTOM)))

        # Cloud
        #blit_alpha(WORLD.surface,cloud1,(c1p,50),128)
        #blit_alpha(WORLD.surface, cloud2, (c2p, 125), 128)
        WORLD.surface.blit(cloud1, (c1p, 50))
        WORLD.surface.blit(cloud2, (c2p, 125))
        c1p += 2
        c2p -= 1.5

        if c1p > TILESIZE*FRAMEWIDTH:
            c1p = -50

        if c2p < -50:
            c2p = 50+(TILESIZE*FRAMEWIDTH)

        # Castle
        WORLD.surface.blit(image, (0,0))

        # Character Selection
        c1 = pygame.image.load('resources/menu_sprites/shadow_char.png')
        c1 = pygame.transform.scale(c1, (50,100))
        testPos = TILESIZE * FRAMEWIDTH / 8
        WORLD.surface.blit(c1, (testPos-25, 450))
        WORLD.surface.blit(c1, ((testPos*3)-25, 450))
        WORLD.surface.blit(c1, ((testPos*5)-25, 450))
        WORLD.surface.blit(c1, ((testPos*7)-25, 450))



    # Update display
    pygame.display.update()
    mainClock.tick(30)  # fps / clock speed

    # END WHILE LOOP
