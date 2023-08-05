"""
A class to handle color for my program
"""


class Color:
    def __init__(self, r: int, g: int, b: int):
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            self.r = r
            self.g = g
            self.b = b
        else:
            raise ValueError('r, g, b values out of range')

    def generate(self, tp):
        # if self.r == tp[0] and self.g == tp[1] and self.b == tp[2]:
        #     return u""
        self.r, self.g, self.b = tp
        return self.__str__()

    def to_tuple(self):
        return self.r, self.g, self.b

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b


class ForegroundColor(Color):
    def __str__(self):
        return u"\u001b[38;2;{};{};{}m".format(self.r, self.g, self.b)


class BackgroundColor(Color):
    def __str__(self):
        return u"\u001b[48;2;{};{};{}m".format(self.r, self.g, self.b)
