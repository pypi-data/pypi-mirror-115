import os
import sys

from gg import InputHandler
from gg import Screen
from gg import Updatable


class Game(Updatable):
    def __init__(self, screen: Screen):
        os.system('clear')
        sys.stdout.write(u"\x1b[?25l")
        self.inp = InputHandler()
        self.score = 0
        self.time = 0
        self.screen = screen
        self.shape = self.screen.shape

    @staticmethod
    def end():
        sys.stdout.write(u"\u001b[0m\x1b[?25h")
        exit(0)
