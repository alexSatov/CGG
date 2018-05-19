from math import inf, sqrt
from typing import Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

from chart import Chart
from task import Task


def f(x: float, y: float) -> float:
    return x * y


# isometry
# def coord_x(x: float, y: float) -> float:
#     return (y - x) * sqrt(3) / 2
#
#
# def coord_y(x: float, y: float, z: float) -> float:
#     return (x + y) / 2 - z

# dimetry
def coord_x(x: float, y: float) -> float:
    return -x / (2 * sqrt(2)) + y


def coord_y(x: float, y: float, z: float) -> float:
    return x / (2 * sqrt(2)) - z


class Task5(Task):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.init_ui()

    def init_ui(self) -> None:
        self.options_bar \
            .with_int_options_v(800, 600, 'width', 'height') \
            .with_int_options_v(-5, 5, 'a', 'b') \
            .with_int_options_v(-5, 5, 'c', 'd') \
            .with_button('Нарисовать', self.draw_chart) \
            .with_image('images\\task5.png')

    def parse_input(self) -> None:
        self.width = int(self.options_bar.v_options[0].top.input.text())
        self.height = int(self.options_bar.v_options[0].bottom.input.text())
        self.a = int(self.options_bar.v_options[1].top.input.text())
        self.b = int(self.options_bar.v_options[1].bottom.input.text())
        self.c = int(self.options_bar.v_options[1].top.input.text())
        self.d = int(self.options_bar.v_options[1].bottom.input.text())

    def valid(self) -> bool:
        return self.width > 0 and self.height > 0 and self.a < self.b and self.c < self.d

    def create_chart(self) -> Chart:
        mx, my = self.width, self.height
        n, m = 40, mx * 2
        top, bottom = self.init_horizons(mx, my)
        max_x, max_y, min_x, min_y = self.calc_boundaries(n, m)

        chart = Chart(self.width, self.height)
        chart.image.fill(Qt.white)

        painter = chart.create_painter()
        blue_pen, red_pen = QPen(Qt.blue, 2), QPen(Qt.red, 2)

        for i in range(n):
            x = self.b + i * (self.a - self.b) / n

            for j in range(m):
                y = self.d + j * (self.c - self.d) / m
                z = f(x, y)
                xx = coord_x(x, y)
                yy = coord_y(x, y, z)
                xx = int((xx - min_x) / (max_x - min_x) * mx)
                yy = int((yy - min_y) / (max_y - min_y) * my)

                if yy > bottom[xx]:
                    painter.setPen(red_pen)
                    painter.drawPoint(xx, yy)
                    bottom[xx] = yy

                if yy < top[xx]:
                    painter.setPen(blue_pen)
                    painter.drawPoint(xx, yy)
                    top[xx] = yy

        painter.end()

        return chart

    def calc_boundaries(self, n: int, m: int) -> Tuple[float, float, float, float]:
        max_x, max_y, min_x, min_y = -inf, -inf, inf, inf

        for i in range(n):
            x = self.b + i * (self.a - self.b) / n

            for j in range(m):
                y = self.d + j * (self.c - self.d) / m
                z = f(x, y)
                xx = coord_x(x, y)
                yy = coord_y(x, y, z)

                if xx > max_x:
                    max_x = xx
                if yy > max_y:
                    max_y = yy
                if xx < min_x:
                    min_x = xx
                if yy < min_y:
                    min_y = yy

        return max_x, max_y, min_x, min_y

    @staticmethod
    def init_horizons(mx: int, my: int) -> Tuple[list, list]:
        top, bottom = [], []

        for i in range(mx + 1):
            top.append(my)
            bottom.append(0)

        return top, bottom
