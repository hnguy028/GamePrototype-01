# Meta Class - forces children to implement a move method
class BaseMob(type):
    def __new__(cls, name, bases, body):
        if name != 'Mob' and 'move' not in body:
            raise TypeError(str(name) + " must implement move")
        return super().__new__(cls, name, bases, body)

# Base Class - defines methods and init variables that are constant for all subclasses
class Mob(metaclass=BaseMob):
    def __init__(self, health):
        self.health = health


    def foo(self):
        print(self.sentence)

# Subclass - for each type of Mob
class Zombie(Mob):
    def __init__(self, health):
        super().__init__(health)

    def move(self):
        self.foo()
        print("END")

z = Zombie(" world")
z.move()