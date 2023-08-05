class Renderable:
    """
    Every renderable must have a width and a height
    For our purposes it would have a rect box
    It must have a render method to be called with a screen
    the position onto which it should be rendered
    """

    def width(self):
        """
        Every renderable must have a definitive height
        :return: The width of the renderable
        """
        pass

    def height(self):
        """
        Every renderable must have a definitive height
        :return: the height of the renderable
        """
        pass

    def shape(self):
        """
        Every renderable must have a definitive shape
        :return: np.array of shape
        """
        pass

    def render(self, screen):
        """
        Every renderable must be able to render itself on a screen
        :param screen: the screen object
        :param pos: the position to render
        :return: nothing
        """
        pass


class Updatable:

    def update(self, timestamp):
        pass
