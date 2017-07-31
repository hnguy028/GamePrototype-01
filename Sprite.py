from includes import *

class Sprite( pygame.sprite.Sprite ):

    def __init__(self, image, pos=(0,0)):
        super(Sprite, self).__init__()
        self.image = image
        self.pos = pos

    def draw(self, surface, pos=(-1,-1)):
        if pos == (-1,-1):
            surface.blit(self.image, self.pos)
        else:
            surface.blit(self.image, pos)

    def drawIcon(self, surface, pos, width, height):
        surface.blit(pygame.transform.scale(self.image, (width, height)), pos)
