import numpy as np
from gg import Scene
from gg.utils import Pos, Vel

from .alien import Alien
from .background import DiscoBg
from .ball import Ball
from .bricks import GlassBrick, RainbowBrick, Brick
from .bullet import PaddleBullet, AlienBullet
from .paddle import Paddle
from .powerup import LongPaddle, ShortPaddle, ShootPaddle, GrabPaddle, SpeedBall, ThruBall


class Level(Scene):
    def __init__(self, game, *args, **kwargs):
        self.game = game
        super(Level, self).__init__(self.game.shape, *args, **kwargs)
        self.paddle = Paddle(self, pos=Pos([self.bottom, (self.width // 4) * 2 - 2]))
        self.background = DiscoBg(self, self.game.shape, pos=Pos([0, 0]))
        self.bricks = []
        self.balls = []
        self.powerups = []
        self.bullets = []
        self.gen()

    def gen(self):
        # pass
        self.generate_bricks()
        ball_pos = self.paddle.pos + Pos([-1, np.random.randint(0, self.paddle.width // 2) * 2])
        self.balls.append(Ball(self, pos=ball_pos, vel=Vel([0, 0])))
        self.add(*self.bricks, self.background, self.paddle, *self.balls)

    def iter_balls(self):
        for it in self.balls:
            if it.is_active():
                yield it

    def iter_bricks(self):
        for it in self.bricks:
            if it.is_active():
                yield it

    def iter_powerups(self):
        for it in self.powerups:
            if it.is_active():
                yield it

    def iter_bullets(self):
        for it in self.bullets:
            if it.is_active():
                yield it

    def add_paddle_bullet(self, pos, vel):
        bullet = PaddleBullet(self, pos=pos, vel=vel)
        self.bullets.append(bullet)
        self.add(bullet)

    def add_powerup(self, pos, vel):
        rand = np.random.randint(0, 6)
        if rand == 0:
            power = LongPaddle(self, pos=pos, vel=vel)
        elif rand == 1:
            power = ShortPaddle(self, pos=pos, vel=vel)
        elif rand == 2:
            power = ShootPaddle(self, pos=pos, vel=vel)
        elif rand == 3:
            power = ThruBall(self, pos=pos, vel=vel)
        elif rand == 4:
            power = SpeedBall(self, pos=pos, vel=vel)
        else:
            power = GrabPaddle(self, pos=pos, vel=vel)
        self.powerups.append(power)
        self.add(power)

    def update(self, timestamp):
        super(Level, self).update(timestamp)
        self.balls = [x for x in self.iter_balls()]
        self.bullets = [x for x in self.iter_bullets()]
        self.bricks = [x for x in self.iter_bricks()]
        self.powerups = [x for x in self.iter_powerups()]
        if timestamp > 200 and timestamp % 50 == 0:
            for x in self.iter_bricks():
                x.move(Pos([1, 0]))
        if len(self.balls) == 0:
            self.game.lives -= 1
            ball_pos = self.paddle.pos + [-1, np.random.randint(0, self.paddle.width // 2) * 2]
            self.balls.append(
                Ball(self, pos=ball_pos, vel=Vel([0, 0]))
            )
            self.add(*self.balls)

    def receive_input(self, char):
        if char in ['j', 'l']:
            direction = -4 if char == 'j' else 4
            # print(direction)
            direction = min(self.right - self.paddle.right, direction)
            # print(direction)
            direction = max(self.left - self.paddle.left, direction)
            # print(direction)
            self.paddle.move(Pos([0, direction]))
            for it in self.iter_balls():
                if it.on_paddle:
                    it.move(Pos([0, direction]))
        elif char == 'k':
            for it in self.iter_balls():
                it.on_paddle = False
                it.set_launch_angle(self.paddle.get_ball_angle(it.x))
        elif char == 's':
            if self.paddle.state['shooting']:
                self.add_paddle_bullet(Pos(self.paddle.pos + Pos([0, 2])), Vel([-1, 0]))


class Level1(Level):
    def generate_bricks(self):
        for it in range(7):
            self.bricks.append(
                RainbowBrick(self, pos=Pos([4, 4 + it * RainbowBrick.SHAPE[1]]))
            )
        for it in range(7):
            self.bricks.append(
                GlassBrick(self, pos=Pos(
                    [4 + 1 * GlassBrick.SHAPE[0], 4 + it * GlassBrick.SHAPE[1]]
                ))
            )

    def update(self, timestamp):
        super(Level1, self).update(timestamp)
        for x in self.iter_bricks():
            if x.bottom >= self.bottom - 2:
                return 'FAIL'
        if len(self.bricks) == 0:
            return 'PASS'


class Level2(Level):
    def generate_bricks(self):

        y = 1
        # Last Row
        for it in range(3):
            self.bricks.append(
                GlassBrick(self, pos=Pos(
                    [y, 4 + (2 * it + 1) * GlassBrick.SHAPE[1]]
                ))
            )

        for it in range(4):
            self.bricks.append(
                RainbowBrick(self, pos=Pos(
                    [y, 4 + 2 * it * RainbowBrick.SHAPE[1]]
                ))
            )

        y += GlassBrick.SHAPE[0]

        # Second Row
        for it in range(3):
            self.bricks.append(
                RainbowBrick(self, pos=Pos(
                    [y, 4 + (2 * it + 1) * RainbowBrick.SHAPE[1]]
                ))
            )

        for it in range(4):
            self.bricks.append(
                Brick(self, pos=Pos(
                    [y, 4 + 2 * it * Brick.SHAPE[1]]
                ))
            )
        y += GlassBrick.SHAPE[0]

        # First Row
        for it in range(3):
            self.bricks.append(
                GlassBrick(self, pos=Pos(
                    [y, 4 + (2 * it + 1) * GlassBrick.SHAPE[1]]
                ))
            )

        for it in range(4):
            self.bricks.append(
                RainbowBrick(self, pos=Pos(
                    [y, 4 + 2 * it * RainbowBrick.SHAPE[1]]
                ))
            )

    def update(self, timestamp):
        super(Level2, self).update(timestamp)
        for x in self.iter_bricks():
            if x.bottom >= self.bottom - 2:
                return 'FAIL'
        if len(self.bricks) == 0:
            return 'PASS'


class AlienLevel(Level):
    def __init__(self, *args, **kwargs):
        super(AlienLevel, self).__init__(*args, **kwargs)
        # print(self.paddle.pos)
        self.alien = Alien(self, pos=Pos([0, (self.width // 4) * 2 - 2]))
        self.add(self.alien)

    def generate_bricks(self):
        pass

    def add_powerup(self, pos, vel):
        pass

    def add_paddle_bullet(self, pos, vel):
        pass

    def add_layer(self):
        for x in self.iter_bricks():
            x.move(Pos([GlassBrick.SHAPE[0], 0]))
        y = self.alien.bottom
        to_add = []
        # First Row
        for it in range(3):
            to_add.append(
                GlassBrick(self, pos=Pos(
                    [y, 4 + (2 * it + 1) * GlassBrick.SHAPE[1]]
                ))
            )

        for it in range(4):
            to_add.append(
                RainbowBrick(self, pos=Pos(
                    [y, 4 + 2 * it * RainbowBrick.SHAPE[1]]
                ))
            )
        self.bricks += to_add
        self.add(*to_add)

    def add_alien_bullet(self, pos, vel):
        # print(pos)
        bullet = AlienBullet(self, pos=pos, vel=vel)
        self.bullets.append(bullet)
        self.add(bullet)

    def receive_input(self, char):
        super(AlienLevel, self).receive_input(char)
        if char in ['j', 'l']:
            direction = -4 if char == 'j' else 4
            direction = min(self.right - self.paddle.right, direction)
            direction = max(self.left - self.paddle.left, direction)
            self.alien.move(Pos([0, direction]))

    def update(self, timestamp):
        if not self.alien.is_active():
            return 'PASS'
        return super(AlienLevel, self).update(timestamp)
