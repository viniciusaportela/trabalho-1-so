from random import randint


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Utils:
    @staticmethod
    def get_random_position():
        return Position(
            Utils.__gen_random_position(),
            Utils.__gen_random_position()
        )

    @staticmethod
    def __gen_random_position():
        return randint(0, 9)
