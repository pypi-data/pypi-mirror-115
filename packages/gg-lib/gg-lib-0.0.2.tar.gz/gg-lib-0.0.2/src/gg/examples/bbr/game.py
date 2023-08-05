from time import perf_counter

import numpy as np
from gg import ForegroundColor, BackgroundColor
from gg import Game

from .level import Level1, Level2, AlienLevel
from .splash_screen import SplashScreen


class BrickBreaker(Game):
    def __init__(self, *args, **kwargs):
        super(BrickBreaker, self).__init__(*args, **kwargs)
        self.total_lives = 10
        self.lives = self.total_lives
        self.levels = [Level1(self), Level2(self), AlienLevel(self)]
        self.level_id = 0
        self.level = self.levels[self.level_id]
        self.current_scene = self.level
        self.frame = 0

    def lives_repr(self):
        return ''.join(
            [u'🤎 ' for i in range(self.lives)] + [u'🤍 ' for i in range(5 - self.lives)])

    def show_transition(self):
        self.screen.clear()
        for i in range(30):
            if i > 0:
                self.print_stats()
            tr = SplashScreen(self, f"""\nLevel: {self.level_id + 1}\n""")
            self.update(i)
            tr.render(self.screen)
            res = self.screen.display()

    def next_level(self):
        self.level_id += 1
        if self.level_id == len(self.levels):
            self.passed()
        self.level = self.levels[self.level_id]
        self.lives = self.total_lives
        self.current_scene = self.level

    def print_stats(self):
        print(str(BackgroundColor(0, 0, 0)) + str(ForegroundColor(255, 255, 255)))
        print('Score:', self.score)
        print('Time: {:.1f}s'.format(self.frame * 0.1))
        print('Lives:', self.lives_repr())

    def passed(self):
        self.screen.clear()
        for i in range(30):
            if i > 0:
                self.print_stats()
            tr = SplashScreen(self, f"""\nYou won, gg\n""")
            self.update(i)
            tr.render(self.screen)
            res = self.screen.display()
        self.end()

    def fail(self):
        self.screen.clear()
        for i in range(30):
            if i > 0:
                self.print_stats()
            tr = SplashScreen(self, f"""\nYou lost, git gud\n""")
            self.update(i)
            tr.render(self.screen)
            res = self.screen.display()
        self.end()

    def exec_(self):
        times = np.zeros(100)
        render = np.zeros((100, 4))
        self.show_transition()
        while True:
            st = perf_counter()
            self.print_stats()
            if self.inp.is_available():
                c = self.inp.getch()
                if c == 'n':
                    self.next_level()
                    self.show_transition()
                    continue
                self.current_scene.receive_input(c)
                self.inp.clear()
            res = self.current_scene.update(self.frame)
            if res == 'FAIL':
                self.fail()
            elif res == 'PASS':
                self.next_level()
                self.show_transition()
                continue
            self.current_scene.render(self.screen)
            nd = perf_counter()
            res = self.screen.display()
            if self.lives == 0:
                break
            times[self.frame % 100] = nd - st
            render[self.frame % 100] = res
            self.frame += 1
        self.fail()
