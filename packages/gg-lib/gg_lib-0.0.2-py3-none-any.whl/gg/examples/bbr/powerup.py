from gg import Sprite
from gg.utils import load_sprite, Vel

from .ball import BoxedMovingMixin
from .sprites import powerup


class PowerUp(BoxedMovingMixin, Sprite):
    def __init__(self, scene, *args, **kwargs):
        super(PowerUp, self).__init__(self.sprite, scene, *args, **kwargs)
        self.vel = Vel(kwargs.get('vel')) / 2
        self.fill_foreground((255, 255, 255))
        self.alpha = True
        self.acc = 0.05

    def update(self, timestamp):
        self.vel += Vel([self.acc, 0])
        self.vel[0] = max(self.vel[0], 1.5)
        self.box_constraints()
        self.move(self.vel)
        # if self.bottom_hit():
        #     self.deactivate()


class PaddlePowerUp(PowerUp):
    def __init__(self, *args, **kwargs):
        super(PaddlePowerUp, self).__init__(*args, **kwargs)

    def mutate(self, paddle, timestamp):
        pass


class BallPowerUp(PowerUp):
    def __init__(self, *args, **kwargs):
        super(BallPowerUp, self).__init__(*args, **kwargs)

    def mutate(self, ball, timestamp):
        pass


class ScenePowerUp(PowerUp):
    def __init__(self, *args, **kwargs):
        super(ScenePowerUp, self).__init__(*args, **kwargs)

    def mutate(self, scene, timestamp):
        pass


class LongPaddle(PaddlePowerUp):
    sprite = load_sprite(powerup['long'])
    SHAPE = sprite.shape

    def mutate(self, paddle, timestamp):
        paddle.set_long(timestamp)


class ShortPaddle(PaddlePowerUp):
    sprite = load_sprite(powerup['short'])
    SHAPE = sprite.shape

    def mutate(self, paddle, timestamp):
        paddle.set_short(timestamp)


class GrabPaddle(PaddlePowerUp):
    sprite = load_sprite(powerup['grab'])
    SHAPE = sprite.shape

    def mutate(self, paddle, timestamp):
        paddle.set_grab(timestamp)


class ShootPaddle(PaddlePowerUp):
    sprite = load_sprite(powerup['shoot'])
    SHAPE = sprite.shape

    def mutate(self, paddle, timestamp):
        paddle.set_shoot(timestamp)


class ThruBall(BallPowerUp):
    sprite = load_sprite(powerup['thru'])
    SHAPE = sprite.shape

    def mutate(self, ball, timestamp):
        ball.set_thru(timestamp)


class SpeedBall(BallPowerUp):
    sprite = load_sprite(powerup['mul'])
    SHAPE = sprite.shape

    def mutate(self, ball, timestamp):
        ball.set_mul(timestamp)

# class LevelModifier(PowerUp):
#     class Types:
#         MULTI_BALL
#
#
#
# class BallModifier(PowerUp):
#     class Types:
#         THRU_BALL
#         FAST_BALL
#
#
# class PaddleModifier(PowerUp):
#     class Types:
#         PADDLE_LONG
#         PADDLE_SHORT
#         PADDLE_GRAB
#         PADDLE_SHOOT
