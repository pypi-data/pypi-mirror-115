import numpy as np


def load_sprite(rep):
    arr = rep.split("\n")[1:-1]
    n = len(max(arr, key=len))
    return np.array([list(x + (' ' * (n - len(x)))) for x in arr])


def load_sprites(rep):
    return list(map(load_sprite, rep))


def remap(_pos):
    y, x = map(round, _pos)
    x = (x >> 1) << 1  # always even position render
    return y, x


def collides(rect1, rect2):
    if rect1.x < rect2.x + rect2.width and \
            rect1.x + rect1.width > rect2.x and \
            rect1.y < rect2.y + rect2.height and \
            rect1.y + rect1.height > rect2.y:
        return True
    return False


def Pos(_pos, *args, **kwargs):
    kwargs['dtype'] = 'f'
    return np.array(_pos, *args, **kwargs)


def Vel(_vel, *args, **kwargs):
    return Pos(_vel, *args, **kwargs)
