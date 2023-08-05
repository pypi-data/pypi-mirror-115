from gg import MovingMixin, Sprite
from gg.utils import load_sprite, Vel

from .sprites import bullet


class Bullet(MovingMixin, Sprite):
    def __init__(self, scene, *args, **kwargs):
        super(Bullet, self).__init__(self.sprite, scene, *args, **kwargs)
        self.vel = Vel([1, 0])
        self.fill_foreground((255, 255, 255))
        self.alpha = True

    def update(self, timestamp):
        self.move(self.vel)


class AlienBullet(Bullet):
    sprite = load_sprite(bullet[0])
    SHAPE = sprite.shape

    def __init__(self, *args, **kwargs):
        super(AlienBullet, self).__init__(*args, **kwargs)
        self.vel = Vel([1, 0])

    def update(self, timestamp):
        if self.bottom == self.scene.paddle.top and \
                self.scene.paddle.left <= self.left <= self.scene.paddle.right:
            self.scene.game.lives -= 1
        self.move(self.vel)


class PaddleBullet(Bullet):
    sprite = load_sprite(bullet[1])
    SHAPE = sprite.shape

    def __init__(self, *args, **kwargs):
        super(PaddleBullet, self).__init__(*args, **kwargs)
        self.vel = Vel([-1, 0])

    def update(self, timestamp):
        for target in self.scene.iter_bricks():
            if self.top == target.bottom:
                self.deactivate()
                return

        self.move(self.vel)
