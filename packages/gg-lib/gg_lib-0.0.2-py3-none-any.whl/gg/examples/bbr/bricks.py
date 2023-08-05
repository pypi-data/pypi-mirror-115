import numpy as np
from gg import Sprite
from gg.utils import load_sprite, load_sprites

from .ball import Ball
from .sprites import brick, glass


class Brick(Sprite):
    sprite = load_sprite(brick)
    SHAPE = sprite.shape

    def __init__(self, scene, *args, **kwargs):
        super(Brick, self).__init__(self.sprite, scene, *args, **kwargs)
        self.fill_foreground((255, 0, 0))
        self.alpha = True

    def hit(self, ball):
        if ball.thru:
            self.deactivate()


class GlassBrick(Sprite):
    SPRITES = load_sprites(glass)
    COLORS = [
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 0)
    ]
    SHAPE = SPRITES[0].shape

    def __init__(self, scene, *args, **kwargs):
        self.state = 0
        super(GlassBrick, self).__init__(self.SPRITES[self.state], scene, *args, **kwargs)
        self.fill_foreground(self.COLORS[self.state])
        self.alpha = True

    def hit(self, ball):
        if isinstance(ball, Ball):
            if ball.state['thru']:
                self.deactivate()
                return
        self.scene.game.score += 100
        self.state += 1
        # if True:
        # print(ball.vel)
        # print("hi")
        if isinstance(ball, Ball):
            self.scene.add_powerup(self.pos + [4, 6], ball.vel)
        if self.state == 3:
            self.scene.game.score += 100
            self.deactivate()
        else:
            self.blit(self.SPRITES[self.state])
            self.fill_foreground(self.COLORS[self.state])


class RainbowBrick(GlassBrick):
    RAINBOW_COLORS = [
        (148, 0, 211),
        (75, 0, 130),
        (0, 0, 255),
        (0, 255, 0),
        (255, 255, 0),
        (255, 127, 0),
        (255, 0, 0),
    ]

    def __init__(self, *args, **kwargs):
        super(RainbowBrick, self).__init__(*args, **kwargs)
        self.rainbow = True
        self.init = np.random.randint(0, 7)

    def hit(self, ball):
        if self.rainbow:
            self.rainbow = False
        super(RainbowBrick, self).hit(ball)

    def update(self, timestamp):
        if self.rainbow:
            state = (timestamp // 2 + self.init) % 7
            self.fill_foreground(self.RAINBOW_COLORS[state])
