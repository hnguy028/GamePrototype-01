import pygame
import pyganim

class Player:
    def __init__(self, world, character, health, magic, coins, direction):
        # player images
        self.front_facing = pygame.image.load('characters/%s/char_front.png' % character)
        self.back_facing = pygame.image.load('characters/%s/char_back.png' % character)
        self.right_facing = pygame.image.load('characters/%s/char_right.png' % character)
        self.left_facing = pygame.transform.flip(self.right_facing, True, False)

        # player's x,y coordinates on the current map/room
        self.x = world.playerSpawn.x % world.widthPixels
        self.y = world.playerSpawn.y % world.widthPixels
        self.direction = direction  # initial stance
        self.running = self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False

        # get sprite's pixel size
        self.width, self.height = self.front_facing.get_size()

        # player stats
        self.health = health
        self.magic = magic
        self.coins = coins

        self.walkRate = 10
        self.runRate = 1

        # creating the PygAnimation objects for walking/running in all directions
        animTypes = 'back_run back_walk front_run front_walk right_run right_walk'.split()
        self.animObjs = {}
        for animType in animTypes:
            imagesAndDurations = [('characters/%s/char_%s.%s.png' % (character, animType, str(num).rjust(3, '0')), 0.1)
                                  for num in range(6)]
            self.animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)

        # create the right-facing sprites by copying and flipping the left-facing sprites
        self.animObjs['left_walk'] = self.animObjs['right_walk'].getCopy()
        self.animObjs['left_walk'].flip(True, False)
        self.animObjs['left_walk'].makeTransformsPermanent()
        self.animObjs['left_run'] = self.animObjs['right_run'].getCopy()
        self.animObjs['left_run'].flip(True, False)
        self.animObjs['left_run'].makeTransformsPermanent()

        # TODO : might need to move conductor to the game loop
        self.moveConductor = pyganim.PygConductor(self.animObjs)
