import numpy as np

from gg import Surface


class DiscoBg(Surface):
    def __init__(self, scene, shape, pos, *args, **kwargs):
        super(DiscoBg, self).__init__(shape, scene, *args, **kwargs)
        self.pos = pos
        self.z = -1

    def update(self, timestamp):
        timestamp *= 2
        ii = (50 - 1 - timestamp % 50) if timestamp // 50 & 1 else timestamp % 50
        self.blit(back=np.array([
            [(ii + col, 0, ii + row) for col in range(self.width)] for row in range(self.height)
        ]))


class PlainBg(Surface):
    def __init__(self, scene, shape, pos, *args, **kwargs):
        super(PlainBg, self).__init__(shape, scene, *args, **kwargs)
        self.pos = pos
        self.z = -1
        self.fill_background((0, 0, 0))
        self.fill_foreground((255, 255, 255))
