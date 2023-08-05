from gg import Scene, Sprite, Pos
from gg.utils import load_sprite

from .background import PlainBg


class TextMessage(Sprite):

    def __init__(self, scene, message, *args, **kwargs):
        self.sprite = load_sprite(message)
        super(TextMessage, self).__init__(self.sprite, scene, *args, **kwargs)
        self.fill_foreground((255, 255, 255))
        self.alpha = True


class SplashScreen(Scene):
    def __init__(self, game, message, *args, **kwargs):
        self.game = game
        super(SplashScreen, self).__init__(self.game.shape, *args, **kwargs)
        self.background = PlainBg(self, self.game.shape, pos=Pos([0, 0]))
        self.message = TextMessage(self, message,
                                   pos=Pos([self.bottom // 2, self.left + (self.width // 4) * 2]))
        self.add(self.message)
