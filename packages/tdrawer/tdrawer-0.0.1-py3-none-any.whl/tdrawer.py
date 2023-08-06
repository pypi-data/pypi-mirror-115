import csv

import _tdrawer as _tdrawer

drawer = _tdrawer.lib
__ffi = _tdrawer.ffi


# wrappers
def cf(fn):
    return __ffi.callback("unsigned int(long long, long long, struct rect *rect)")(fn)


def yf(fn):
    return __ffi.callback("double(double)")(fn)


def cmf(fn):
    return __ffi.callback("unsigned int(double, double)")(fn)


from typing import Tuple, Callable, List, Optional
from abc import ABC, abstractmethod

red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
aqua = 0x7fffd4


class Drawable(ABC):
    options = {
        'color': red
    }

    @abstractmethod
    def to_points(self) -> Tuple[List[float], List[float]]:
        pass

    def to_color(self, x: float, y: float) -> int:
        color = self.options['color']
        if callable(color):
            return color(x, y)
        return color


class DrawableFunction1D(Drawable):
    result: Optional[Tuple[List[float], List[float]]]

    def __init__(self, function: Callable, start: float = -1, end: float = 1, dx: float = 0.01, options=None):
        self.function = function
        self.start = start
        self.end = end
        self.dx = dx
        self.result = None
        if options is not None:
            self.options = {**self.options, **options}

    def to_points(self) -> Tuple[List[float], List[float]]:
        if self.result is not None:
            return self.result
        self.result = ([], [])
        x = self.start
        while x <= self.end:
            self.result[0].append(x)
            self.result[1].append(self.function(x))
            x += self.dx
        return self.result


class Points(Drawable):
    def __init__(self, xs: List[float], ys: List[float], **kwargs):
        self.xs = xs
        self.ys = ys
        self.options = {**self.options, **kwargs}

    def to_points(self) -> Tuple[List[float], List[float]]:
        return self.xs, self.ys

    @staticmethod
    def from_csv(filename: str) -> 'Points':
        xs = []
        ys = []
        with open(filename) as f:
            for line in csv.reader(f, delimiter=','):
                xs.append(float(line[0]))
                ys.append(float(line[1]))

        return Points(xs, ys)


class Canvas:
    options = {
        "lazy": True
    }

    __xs: List[float]
    __ys: List[float]
    __sep: List[int]

    __drawables: List[Drawable]

    def __init__(self, options=None):
        self.__xs = []
        self.__ys = []
        self.__sep = [0]
        self.__drawables = []

        if options is not None:
            self.options = {**self.options, **options}

        drawer.init()

    def set_window_hints(self, title, size: Tuple[int, int] = None):
        if size is None:
            size = (900, 900)
        drawer.setWindowHint(int(size[0]), int(size[1]), title.encode('ascii'))

    def set_edges(self, left: float, right: float, top: float, bottom: float):
        drawer.setCanvasEdge(left, right, top, bottom)

    def eval_drawable(self, drawable: Drawable):
        xs, ys = drawable.to_points()
        self.__xs.extend(xs)
        self.__ys.extend(ys)
        self.__sep.append(self.__sep[-1] + len(xs))

    def add_drawable(self, drawable: Drawable):
        if not self.options['lazy']:
            self.eval_drawable(drawable)
        self.__drawables.append(drawable)

    def simulate(self, dx: float = 0.001, items: int = 1, size: float = 0.01):
        if self.options['lazy']:
            for drawable in self.__drawables:
                self.eval_drawable(drawable)

        def cFunc(c, p, r):
            idx = 0
            for i, r in enumerate(self.__sep):
                if r > p:
                    idx = i - 1
                    break

            return self.__drawables[idx].to_color(self.__xs[p], self.__ys[p])

        length = len(self.__xs)
        drawer.drawBase(self.__xs, self.__ys, length, dx, items, cf(cFunc), size)

    def display(self, size: float = 0.01):
        if self.options['lazy']:
            for drawable in self.__drawables:
                self.eval_drawable(drawable)

        def cFunc(c, p, r):
            idx = 0
            for i, r in enumerate(self.__sep):
                if r > p:
                    idx = i - 1
                    break

            return self.__drawables[idx].to_color(self.__xs[p], self.__ys[p])

        length = len(self.__xs)
        drawer.drawBase(self.__xs, self.__ys, length, 0, length, cf(cFunc), size)

    def __del__(self):
        drawer.stop()


if __name__ == '__main__':
    # canvas = Canvas()
    # canvas.set_edges(0, 1000, 10, 0)
    # canvas.add_function(DrawableFunction1D(lambda x: 9 - 1/100 * x, 0, 1000, dx=0.1, options={
    #     'color': blue
    # }))
    # canvas.add_function(DrawableFunction1D(lambda x: 1/200 * x, 0, 1000, dx=0.1, options={
    #     'color': red
    # }))
    # canvas.display(size=0.1)
    i = +~-~+---+~-~+---+++~+++---+-+~~+-12
    print(i)
