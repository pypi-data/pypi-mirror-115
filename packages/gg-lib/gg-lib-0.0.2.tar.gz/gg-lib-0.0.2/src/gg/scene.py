from .interfaces import Renderable, Updatable
from .mixins import MovingMixin
from .utils import remap, Pos


class Scene(Renderable, Updatable):
    """
    A scene is both renderabe and updatable
    you can have multiple scenes at the same time
    an example of this can be a game scene and a HUD or score scene
    The shape of a scene also does not change once defined

    A scene as a definitive shape width height
    A scene can also be updated
    """

    def __init__(self, shape: tuple, *args, **kwargs):
        super(Scene, self).__init__(**kwargs)
        self._shape = shape
        self._fixed_entities = []
        self._moving_entities = []
        self.pos = kwargs.get('pos', Pos([0, 0]))

    @property
    def width(self):
        return self._shape[1]

    @property
    def height(self):
        return self._shape[0]

    @property
    def top(self):
        assert hasattr(self, 'pos'), (
            'The position of the object must be defined'
        )
        y, x = remap(self.pos)
        return 0

    @property
    def bottom(self):
        assert hasattr(self, 'pos'), (
            'The position of the object must be defined'
        )
        assert hasattr(self, 'height'), (
            'A Renderable must have a width defined'
        )
        return self.top + self.height

    @property
    def left(self):
        assert hasattr(self, 'pos'), (
            'The position of the object must be defined'
        )
        y, x = remap(self.pos)
        return x

    @property
    def right(self):
        assert hasattr(self, 'pos'), (
            'The position of the object must be defined'
        )
        assert hasattr(self, 'width'), (
            'A Renderable must have a width defined'
        )
        return self.left + self.width

    def add(self, *entities):
        """
        Add an entity to the scene
        this way the scene has control of the generics
        :param entity:
        :return:
        """
        for entity in entities:
            if isinstance(entity, MovingMixin):
                self._moving_entities.append(entity)
            else:
                self._fixed_entities.append(entity)

    def gen(self):
        pass

    def render(self, screen):
        assert self._shape == screen.shape, (
            'Screen and scene sizes donot match'
        )
        self._render_entities(screen)

    def update(self, timestamp):
        self._moving_entities = [x for x in self._moving_entities if x.is_active()]
        self._fixed_entities = [x for x in self._fixed_entities if x.is_active()]
        for entity in self._moving_entities:
            if entity.is_active():
                entity.update(timestamp)
        for entity in self._fixed_entities:
            if entity.is_active():
                entity.update(timestamp)

    def _render_entities(self, screen):
        for entity in self._fixed_entities:
            if entity.is_active():
                entity.render(screen)
        for entity in self._moving_entities:
            if entity.is_active():
                entity.render(screen)
