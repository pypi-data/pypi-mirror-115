import operator
import sys
import time

import numpy as np

from .color import BackgroundColor, ForegroundColor
from .utils import remap

bc = BackgroundColor(0, 0, 0)
fc = ForegroundColor(255, 255, 255)


class Screen:

    def __init__(self, shape):
        h, w = shape
        self._shape = shape
        self._back = np.full((h, w, 3), np.array([0, 0, 0]), dtype='i2')
        self._char = np.full((h, w), ' ', dtype='<U1')
        self._front = np.full((h, w, 3), np.array([255, 255, 255]), dtype='i2')
        self._bg_buffer = []
        self._char_buffer = []
        self._fg_buffer = []

    @property
    def width(self):
        return self._shape[1]

    @property
    def height(self):
        return self._shape[0]

    def clear(self):
        self._front.fill(0)
        self._back.fill(0)
        self._char.fill(' ')

    def front(self):
        return self._front

    def back(self):
        return self._back

    def char(self):
        return self._char

    @staticmethod
    def flush(self):
        sys.stdout.write("\033[0;0H")

    @property
    def shape(self):
        return self._shape

    def render(self, y, x, renderable):
        """
        Render the surface at position x, y
        :param x: x position of the renderable
        :param y: y position of the renderable
        :param renderable: the renderable
        :return: nothing
        """
        from gg.surface import Surface
        if isinstance(renderable, Surface):
            if not renderable.is_trans():
                self._bg_buffer.append(
                    (renderable.z, (y, x), renderable.get_bg()))
            self._fg_buffer.append((renderable.z, (y, x), renderable.get_fg()))
            self._char_buffer.append(
                (renderable.z, (y, x), renderable.get_char()))

    def iter_bg_buffer(self):
        for i in self._bg_buffer:
            yield i

    def iter_fg_buffer(self):
        for i in self._fg_buffer:
            yield i

    def iter_char_buffer(self):
        for i in self._char_buffer:
            yield i

    def update(self):
        self._bg_buffer_update()
        self._fg_buffer_update()
        self._char_buffer_update()

    def _char_buffer_update(self):
        self._char_buffer.sort(key=operator.itemgetter(0))
        for val in self.iter_char_buffer():
            y, x = remap(val[1])
            height, width = val[2].shape
            if not 0 <= y <= self.height:
                continue
            if not 0 <= x <= self.width:
                continue
            self._char[y:min(self.height, y + height), x: min(self.width, x + width)] = val[2][:min(
                self.height - y, height), :min(self.width - x, width)]

    def _fg_buffer_update(self):
        self._fg_buffer.sort(key=operator.itemgetter(0))
        for val in self.iter_fg_buffer():
            y, x = remap(val[1])
            height, width = val[2].shape[:2]
            if not 0 <= y <= self.height:
                continue
            if not 0 <= x <= self.width:
                continue
            self._front[y:min(self.height, y + height), x: min(self.width, x + width)] = val[2][:min(
                self.height - y, height), :min(self.width - x, width)]

    def _bg_buffer_update(self):
        self._bg_buffer.sort(key=operator.itemgetter(0))
        for val in self.iter_bg_buffer():
            y, x = remap(val[1])
            height, width = val[2].shape[:2]
            if not 0 <= y <= self.height:
                continue
            if not 0 <= x <= self.width:
                continue
            self._back[y:min(self.height, y + height), x: min(self.width, x + width)] = val[2][:min(
                self.height - y, height), :min(self.width - x, width)]

    # def string(self):
    #     bc = BackgroundColor(0, 0, 0)
    #     fc = ForegroundColor(255, 255, 255)
    #     list_of_str = []
    #     for i in range(self.height):
    #         list_of_str.append(
    #             ''.join([
    #                 bc.generate(self._back[i, j]) + fc.generate(self._front[i, j]) +
    #                 self._char[i, j] for j in range(self.width)
    #             ])
    #         )
    #         bc.generate((0, 0, 0))
    #         fc.generate((0, 0, 0))
    #     list_of_str = '\u001b[0m\n'.join(list_of_str)
    #     return list_of_str

    def _clear_buffers(self):
        self._bg_buffer = []
        self._fg_buffer = []
        self._char_buffer = []

    def display(self):
        a = time.perf_counter()
        self._bg_buffer_update()
        self._fg_buffer_update()
        self._char_buffer_update()
        b = time.perf_counter()

        list_of_str = [''.join([
            bc.generate(self._back[i, j]) +
            fc.generate(self._front[i, j]) +
            self._char[i, j] for j in range(self.width)])
            for i in range(self.height)]

        c = time.perf_counter()
        list_of_str = '\u001b[0m\n'.join(list_of_str)
        sys.stdout.write(list_of_str)
        del list_of_str
        sys.stdout.write("\033[0;0H")
        d = time.perf_counter()
        self._clear_buffers()
        e = time.perf_counter()
        return b - a, c - b, d - c, e - d
