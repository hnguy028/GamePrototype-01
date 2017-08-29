class _Movement_Pattern():
    def __init__(self, pattern):
        self.pattern = pattern

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        raise NotImplementedError("")

class Square_Pattern(_Movement_Pattern):
    def __init__(self):
        super().__init__('square_pattern')
        self.counter = 0

    def next(self):
        self.counter += 1
        return self.counter