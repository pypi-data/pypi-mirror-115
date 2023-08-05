from gg import Sprite
from gg import StatefulMixin
from gg.utils import load_sprites, collides

from .powerup import PaddlePowerUp, BallPowerUp
from .sprites import paddle


class Paddle(StatefulMixin, Sprite):
    sprites = load_sprites(paddle)
    SHAPE = sprites[0].shape
    COLORS = [
        (255, 0, 0),
        (0, 0, 255),
        (0, 255, 0)
    ]

    def __init__(self, scene, *args, **kwargs):
        state = {
            'length': 0,
            'length_time': 0,
            'grabbing': False,
            'grab_time': 0,
            'shooting': False,
            'shoot_time': 0,
            'color': 0
        }
        kwargs['state'] = state
        super(Paddle, self).__init__(self.sprites[state['length']], scene, *args, **kwargs)
        self.fill_foreground(self.COLORS[self.state['color']])

    def get_ball_angle(self, x):
        x = round(x)
        dx = ((((x - self.left) >> 1) << 1) - ((self.width >> 2) << 1)) >> 1
        if dx == 0:
            return 90
        elif dx == 1:
            return 60
        elif dx == -1:
            return -60
        elif dx == 2:
            return 45
        elif dx == -2:
            return -45
        elif dx == 3:
            return 30
        elif dx == -3:
            return -30
        else:
            print("fasd", x, dx)
            assert False

    def update_sprite(self):
        self.resize(self.sprites[self.state['length']].shape)
        self.fill_foreground(self.COLORS[self.state['color']])
        self.blit(self.sprites[self.state['length']])

    def reset(self, timestamp):
        self.update_state({
            'length': 0,
            'length_time': timestamp,
            'grabbing': False,
            'grab_time': timestamp,
            'shooting': False,
            'shoot_time': timestamp,
            'color': 0
        })
        self.update_sprite()

    def set_long(self, timestamp):
        self.update_state({'length': 2, 'length_time': timestamp})
        self.update_sprite()

    def set_short(self, timestamp):
        self.update_state({'length': 1, 'length_time': timestamp})
        self.update_sprite()

    def set_grab(self, timestamp):
        self.update_state({'grabbing': True, 'color': 1, 'grab_time': timestamp})
        self.update_sprite()

    def set_shoot(self, timestamp):
        self.update_state({'shooting': True, 'color': 2, 'shoot_time': timestamp})
        self.update_sprite()

    def reset_length(self, timestamp):
        self.update_state({'length': 0, 'length_time': timestamp})
        self.update_sprite()

    def reset_grab(self, timestamp):
        self.update_state({'grabbing': False, 'color': 0, 'grab_time': timestamp})
        self.update_sprite()

    def reset_shoot(self, timestamp):
        self.update_state({'shooting': False, 'color': 0, 'shoot_time': timestamp})
        self.update_sprite()

    def update(self, timestamp):
        if self.state['shooting']:
            print('Paddle shoot:', (self.state['shoot_time'] + 100 - timestamp) * 0.05)
        for target in self.scene.iter_balls():
            if (
                    target.bottom >= self.top and
                    target.vy > 0 and
                    self.left - 1 <= target.left <= self.right + 1
            ) or (collides(target, self)):
                if not self.state['grabbing']:
                    target.set_launch_angle(self.get_ball_angle(target.left))
                else:
                    target.on_paddle = True
                    target.pos[0] = self.top - 1

        for target in self.scene.iter_powerups():
            if (
                    self.top <= target.bottom <= self.bottom and
                    target.vy > 0 and
                    self.left - 1 <= target.left <= self.right + 1
            ) or (collides(target, self)):
                if isinstance(target, PaddlePowerUp):
                    target.mutate(self, timestamp)
                if isinstance(target, BallPowerUp):
                    for ball in self.scene.iter_balls():
                        target.mutate(ball, timestamp)
                target.deactivate()

        if self.state['grabbing'] and timestamp - self.state['grab_time'] > 100:
            self.reset_grab(timestamp)
        if self.state['shooting'] and timestamp - self.state['shoot_time'] > 100:
            self.reset_shoot(timestamp)
        if self.state['length'] and timestamp - self.state['length_time'] > 100:
            self.reset_length(timestamp)
