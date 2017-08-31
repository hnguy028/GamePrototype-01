from NPC_Movement import *
from resource_loader import *
from constants import *
import math

# Base Class - defines methods and init variables that are constant for all subclasses
class Base_NPC():
    def __init__(self, filename, origin, movement_speed, dim):
        # check if subclass has overritten this class
        self._isSubclass()

        self.image_name = filename
        self.origin = origin
        self.pos = origin
        self.movement_speed = movement_speed
        self.width, self.height = dim

        self.image = pygame.transform.scale(pygame.image.load(self.image_name), (self.width, self.height))
        self.move_conductor = None
        self.direction = -1

    # Method to deny intialization of the Mob class
    def _isSubclass(self):
        raise NotImplementedError("Cannot instantiate this class")

    def next(self):
        raise NotImplementedError("Subclass must override this method")

    def move(self, player_pos):
        # call subclass next() method
        self.pos = (self.next(player_pos[0], player_pos[1]))

    def draw(self, surface):
        # TODO : implement conductor animation
        surface.blit(self.image, self.pos)

    def check_collision(self):
        pass

    def get_center(self):
        return self.pos[0] + (self.width // 2), self.pos[1] + (self.height // 2)

class NPC(Base_NPC):
    # no need to check for
    pass

class Mob(Base_NPC):
    def __init__(self, filename, origin, movement_speed, dim, **stats):
        super().__init__(filename, origin, movement_speed, dim)
        self.health = stats['health']
        self.damage = stats['damage']
        self.attack_radius = stats['attack_radius']

    def take_damage(self, dmg):
        self.health = max(0, self.health - dmg)

        # play stagger animation, and bounce back

    # call once health hits 0
    def delete(self):
        # play fade animation, then delete
        pass

#######################################################################################################################
#                                                  NPC Instances                                                      #
#######################################################################################################################
# Subclass - for each type of Mob
class Zombie(Mob):
    def __init__(self, origin, level=1):
        # scale these according to level
        filename = CHARACTER_DIRECTORY + "zombie/0/0.png"
        movement_speed = 3 * level
        dim = (32, 32)

        health = 10
        damage = 5
        attack_radius = 100

        stats = {'level':level, 'health':health, 'damage':damage, 'attack_radius':attack_radius}

        super().__init__(filename, origin, movement_speed, dim, **stats)

        # self.pattern = Square_Pattern(self.movement_speed)
        self.idle_pattern = Idle_Pattern(self.movement_speed)
        self.attack_pattern = Homing_Pattern(self.movement_speed)

    def _isSubclass(self): return True

    def next(self, x, y):
        # euclidean distance
        delta_pos = math.hypot(x - self.pos[0], y - self.pos[1])

        # TODO : mob needs to return to pattern location if player moves out of range?
        # TODO : handle obstacle interactions

        if delta_pos < self.attack_radius:
            # movement behaviour when player is within mob's attack radius
            return self.attack_pattern.next(self_pos=self.pos, player_pos=(x, y))
        else:
            # normal behaviour
            return self.idle_pattern.next(self_pos=self.pos)
