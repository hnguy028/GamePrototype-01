from NPC_Movement import *

# Base Class - defines methods and init variables that are constant for all subclasses
class Mob():
    def __init__(self, filename, health):
        self._isSubclass()
        self.health = health
        self.pos = None
        self.direction = -1

    def _isSubclass(self):
        raise NotImplementedError("Cannot instantiate this class")

    def next(self):
        raise NotImplementedError("Subclass must override this method")

    def move(self):
        self.direction = self.next()

    def draw(self):
        print(self.direction)

# Subclass - for each type of Mob
class Zombie(Mob):
    def __init__(self, filename, health):
        super().__init__(filename, health)
        self.pattern = Square_Pattern()

    def _isSubclass(self): return True

    def next(self):
        return self.pattern.next()

z = Zombie(" world")
z.draw()
z.move()
z.draw()