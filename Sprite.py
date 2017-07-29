from includes import *

class Sprite( pygame.sprite.Sprite ):

    def __init__(self, image, pos=(0,0)):
        super(Sprite, self).__init__()
        self.image = image
        self.pos = pos

    def draw(self, surface):
        surface.blit(self.image, self.pos)