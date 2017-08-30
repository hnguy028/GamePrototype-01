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

class Idle_Pattern(_Movement_Pattern):
    def __init__(self, movement_speed):
        super().__init__('idle_pattern')
        self.movement_speed = 0

    def next(self, **kwargs):
        return kwargs['self_pos']

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
    def __init__(self, movement_speed, vertical):
        super().__init__('linear_pattern')
        self.movement_speed = movement_speed
        self.vertical = vertical
        self.depart = True

    def next(self, **kwargs):
        self_x, self_y = kwargs['self_pos']
        p1_x, p1_y = kwargs['origin']
        p2_x, p2_y = kwargs['destination']

        if self.vertical:
            if self.depart:
                # move towards p2
                pass
            else:
                # move towards p1
                pass

            return self_x, self_y + self.movement_speed
        else:
            if self.depart:
                # move towards p2
                pass
            else:
                # move towards p1
                pass

            return self_x + self.movement_speed, self_y

class Homing_Pattern(_Movement_Pattern):
    def __init__(self, movement_speed):
        super().__init__('homing_pattern')
        self.movement_speed = movement_speed

    def next(self, **kwargs):
        # move towards other at set movement speed
        self_x, self_y = kwargs['self_pos']
        other_x, other_y = kwargs['player_pos']

        x_prime = other_x - self_x
        y_prime = other_y - self_y

        r_prime = math.sqrt(x_prime * x_prime + y_prime * y_prime)

        # movement speed in pixels, ratio = 0 if r_prime is zero
        ratio = 0 if r_prime == 0 else self.movement_speed / r_prime

        # return vector component normalized to movement speed
        return self_x + int(x_prime * ratio), self_y + int(y_prime * ratio)