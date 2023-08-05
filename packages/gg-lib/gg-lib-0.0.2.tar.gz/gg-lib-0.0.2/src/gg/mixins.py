from .utils import Vel


# python Mixin
class MovingMixin:
    """
    A moving generics has a velocity attribute
    This velocity can be manipulated
    velocity is first down and then left
    """

    def __init__(self, *args, **kwargs):
        super(MovingMixin, self).__init__(*args, **kwargs)
        self.vel = kwargs.get('vel', Vel([0, 0]))

    @property
    def vx(self):
        return self.vel[1]

    @property
    def vy(self):
        return self.vel[0]

    def set_vel(self, vel):
        self.vel = vel

    def add_vel(self, vel):
        self.vel += vel
