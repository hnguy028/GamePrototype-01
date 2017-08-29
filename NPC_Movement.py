# TODO : check for exception and error if **kwwargs does not contain the variable name required for next()
import math

class _Movement_Pattern():
    def __init__(self, pattern):
        self.pattern = pattern

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self, **kwargs):
        raise NotImplementedError("")

class Square_Pattern(_Movement_Pattern):
    def __init__(self, movement_speed):
        super().__init__('square_pattern')
        self.movement_speed = movement_speed
        self.counter = 0

    def next(self, **kwargs):
        #self_x, self_y = kwargs['self_x'], kwargs['self_y']
        #width, height = kwargs['width'], kwargs['height']
        #origin = kwargs['origin']



        return self.counter

class Linear_Pattern(_Movement_Pattern):
    def __init__(self, movement_speed):
        super().__init__('linear_patter')
        self.movement_speed = movement_speed

    def next(self, **kwargs):
        # move towards other at set movement speed
        self_x, self_y = kwargs['self_x'], kwargs['self_y']
        other_x, other_y = kwargs['player_x'], kwargs['player_y']

        x_prime = other_x - self_x
        y_prime = other_y - self_y

        r_prime = math.sqrt(x_prime * x_prime + y_prime * y_prime)

        # movement speed in pixels?
        ratio = self.movement_speed / r_prime

        # return vector component normalized to movement speed
        return self_x + int(x_prime * ratio), self_y + int(y_prime * ratio)