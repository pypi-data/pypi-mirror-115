from bbr.sprites import alien
from gg import StatefulMixin, Sprite
from gg.utils import load_sprite, collides, Vel, Pos


class Alien(StatefulMixin, Sprite):
    sprite = load_sprite(alien[1])
    SHAPE = sprite.shape

    def __init__(self, scene, *args, **kwargs):
        state = {
            'done': 0,
            'color': [255, 255, 66]
        }
        kwargs['state'] = state
        super(Alien, self).__init__(self.sprite, scene, *args, **kwargs)
        self.fill_foreground(self.state['color'])

    def update_sprite(self):
        self.fill_foreground(self.state['color'])

    def hit(self, targeet):
        self.state['color'][1] -= 20
        if self.state['color'][1] < 200 and self.state['done'] == 0:
            self.scene.add_layer()
            self.state['done'] += 1
        elif self.state['color'][1] < 100 and self.state['done'] == 1:
            self.scene.add_layer()
            self.state['done'] += 1
        elif self.state['color'] <= 0:
            self.deactivate()
        self.update_sprite()

    def update(self, timestamp):
        for target in self.scene.iter_balls():
            if (target.top == self.bottom or collides(target, self) and target.vy < 0) \
                    or (target.bottom == self.top or collides(target, self) and target.vy > 0):
                if target.left > self.left - 1 and target.right < self.right + 2:
                    self.hit(target)
                    target.switch_y()
                elif target.left == self.left - 1 and target.vx > 0:
                    self.hit(target)
                    target.switch_x()
                    target.switch_y()
                elif target.left == self.right + 1 and target.vx < 0:
                    self.hit(target)
                    target.switch_x()
                    target.switch_y()

            elif (target.left == self.right or collides(target, self) and target.vx < 0) or \
                    (target.right == self.left or collides(target, self) and target.vx > 0):
                if self.top <= target.top <= self.bottom:
                    self.hit(target)
                    target.switch_x()

        if timestamp % 50 == 0:
            self.scene.add_alien_bullet(Pos([self.bottom, self.left + self.width // 2]), Vel([1, 0]))
