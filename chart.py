import matplotlib.pyplot as plt
import numpy
import random


class Curve:

    def __init__(self, values, dx=1.0, name=None, visible=True, x_axis=None):
        assert dx > 0

        self.values = values
        self.dx = dx
        if x_axis is None:
            self.x_axis = [x * self.dx for x in range(len(self.values))]
        else:
            self.x_axis = x_axis

        self.name = name or ""
        self.visible = visible

    def get_derivative(self):
        values = numpy.diff(self.values)
        return Curve(values, self.dx, self.name + "'")

    def get_abs(self):
        return Curve([abs(x) for x in self.values])

    @classmethod
    def from_function(cls, function, interval, dx, name=None, visible=True):
        assert isinstance(interval, range)

        values = [function(x*dx) for x in interval]
        return cls(values, dx, name, visible)


class Chart:

    COLORS = ["#FC9E4F", "#FF1053", "#2274A5", "#2C6E49"]

    def __init__(self, graphics=1, name=None, axes=True):
        assert graphics > 0
        self.graphics = graphics

        self.figure, self.graphs = plt.subplots(graphics)

        if name:
            self.figure.suptitle(name)

        self.choosen_colors = []
        self.curves = []

        self.axes = axes

    def add_curve(self, curve, graph=0):
        assert 0 <= graph < self.graphics

        self.curves.append(curve)

        color = self.get_color() if curve.visible else "w"

        if self.graphics > 1:
            self.graphs[graph].plot(curve.x_axis, curve.values, color, label=curve.name)
        else:
            self.graphs.plot(curve.x_axis, curve.values, color, label=curve.name)

    def display(self):
        # colors, names = [], []
        #
        # for index, curve in enumerate(self.curves):
        #     if curve.visible:
        #         colors.append(index)
        #         names.append(curve.name)

        if self.graphics > 1:
            for i in range(self.graphics):
                self.graphs[i].legend()
                if not self.axes:
                    self.graphs[i].axes.get_xaxis().set_visible(False)
                    self.graphs[i].axes.get_yaxis().set_visible(False)
        else:
            plt.legend()
            if not self.axes:
                self.graphs.axes.get_xaxis().set_visible(False)
                self.graphs.axes.get_yaxis().set_visible(False)

        plt.show()

    def get_color(self):
        if len(self.choosen_colors) < len(Chart.COLORS):
            while True:
                color = random.choice(Chart.COLORS)
                if color not in self.choosen_colors:
                    self.choosen_colors.append(color)
                    return color
        else:
            self.choosen_colors = []
            return self.get_color()