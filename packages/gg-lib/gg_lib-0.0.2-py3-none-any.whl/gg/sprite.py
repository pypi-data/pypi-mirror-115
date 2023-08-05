from .scene import Scene
from .surface import Surface


class Sprite(Surface):
    """
    A sprite is a surface with a definitive representation
    """

    def __init__(self, scene: Scene, chars, *args, **kwargs):
        super(Sprite, self).__init__(scene, chars.shape, *args, **kwargs)
        self.blit(chars)
