from NPC_Movement import *

# Base Class - defines methods and init variables that are constant for all subclasses
class Mob():
    def __init__(self, filename, health):
        self._isSubclass()
        self.health = health
        self.pos = None
        self.width, self.height = 0, 0
        self.image = None
        self.move_conductor = None
        self.direction = -1

    # Method to deny intialization of the Mob class
    def _isSubclass(self):
        raise NotImplementedError("Cannot instantiate this class")

    def next(self):
        raise NotImplementedError("Subclass must override this method")

    def move(self):
        self.pos = (self.next())

    def draw(self, surface):
        print(self.direction)

    def check_collision(self):
        pass

    def check_player(self):
        pass

# Subclass - for each type of Mob
class Zombie(Mob):
    def __init__(self, filename, health, movement_speed):
        super().__init__(filename, health)
        self.pattern = Square_Pattern(movement_speed)

    def _isSubclass(self): return True

    # TODO : one the player is within a certain radius -> change movement behaviour / speed
    def next(self):
        # if within radius
        # note : dont need to check all points of player just a single handle is fine
            # linear pattern.next()
        # else:
        return self.pattern.next()

class Tt():
    def __init__(self, *args):
        #self.t = args[0]
        pass

z = Zombie("", " world", 0)
z.draw("")
z.move()
z.draw("")

pat = Linear_Pattern(9)
x, y = pat.next(self_x=0, self_y=0, player_x=10, player_y=10)
print(x," ",y)