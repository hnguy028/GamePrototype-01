from NPC_Movement import *
from includes import *

# Base Class - defines methods and init variables that are constant for all subclasses
class Mob():
    def __init__(self, filename, health, pos):
        self._isSubclass()
        self.image_name = filename
        self.health = health
        self.pos = pos
        self.width, self.height = 0, 0
        self.image = None
        self.move_conductor = None
        self.direction = -1

    # Method to deny intialization of the Mob class
    def _isSubclass(self):
        raise NotImplementedError("Cannot instantiate this class")

    def next(self):
        raise NotImplementedError("Subclass must override this method")

    def move(self, x, y):
        self.pos = (self.next(x, y))

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), self.pos, 10)

    def check_collision(self):
        pass

    def check_player(self):
        pass

# Subclass - for each type of Mob
class Zombie(Mob):
    def __init__(self, filename, health, movement_speed, pos):
        super().__init__(filename, health, pos)
        self.pattern = Square_Pattern(movement_speed)
        self.homing_pattern = Homing_Pattern(movement_speed)

    def _isSubclass(self): return True

    # TODO : one the player is within a certain radius -> change movement behaviour / speed
    def next(self, x, y):
        # if within radius
        # note : dont need to check all points of player just a single handle is fine
            # linear pattern.next()
        # else:
        return self.homing_pattern.next(self_pos=self.pos, player_pos=(x, y))
        #return self.pattern.next()

class Tt():
    def __init__(self, *args):
        #self.t = args[0]
        pass