from gg import Screen

from .game import BrickBreaker

W = 110
H = 50
SZ = (H, W)


def start():
    game = BrickBreaker(Screen(SZ))
    game.exec_()


if __name__ == '__main__':
    start()
