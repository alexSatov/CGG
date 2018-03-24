from math import sqrt, cos, sin, radians, fabs

from task1 import Task1

from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QRect


class PixelPoint:
    def __init__(self, x, y, unit):
        self.x = round(x * unit)
        self.y = round(y * unit)

    def get_distance(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Task2(Task1):
    def __init__(self, main_window):
        super().__init__(main_window)

    def init_ui(self):
        self.options_bar \
            .with_area() \
            .with_interval(0, 360) \
            .with_int_option('a', 1) \
            .with_button('Нарисовать', self.draw_chart)

        self.setLayout(self.v_layout)

    def parse_input(self):
        ox = int(self.options_bar.area.left_top.x.input.text())
        oy = int(self.options_bar.area.left_top.y.input.text())
        maxx = int(self.options_bar.area.right_bottom.x.input.text())
        maxy = int(self.options_bar.area.right_bottom.y.input.text())
        alpha = int(self.options_bar.interval.alpha.input.text())
        beta = int(self.options_bar.interval.beta.input.text())
        a = int(self.options_bar.options[0].input.text())
        r = self.create_func(a)

        return maxx - ox, maxy - oy, alpha, beta, r

    def create_chart(self, args):
        chart = self.get_chart(args)
        chart = self.add_axis_and_grid(chart, 'φ', 'r')

        return chart

    def get_chart(self, args):
        rad = radians
        width, height, u0, u1, r = args
        x0, y0, unit, = width // 2, height // 2, self.grid_step
        chart = QImage(width, height, QImage.Format_ARGB32)
        painter = QPainter(chart)
        painter.setPen(QPen(Qt.blue, 3))

        u, du, d, a, b = u0, 1, 10, 3, 2
        ru = r(u) if not None else None
        point = PixelPoint(ru * cos(rad(u)), ru * sin(rad(u)), unit) if \
            ru is not None else None

        while u < u1:
            u += du
            ru = r(u)

            if not ru:
                point = None
                continue

            new_point = PixelPoint(ru * cos(rad(u)), ru * sin(rad(u)), unit)

            if fabs(new_point.x) > x0 or fabs(new_point.y) > y0:
                point = None
                continue

            if not point:
                point = new_point
                continue

            if point.get_distance(new_point) > d:
                u -= du
                du /= a
                continue

            if point == new_point:
                u -= du
                du *= b
                continue

            xx0, yy0 = point.x + x0, y0 - point.y
            xx1, yy1 = new_point.x + x0, y0 - new_point.y
            point = new_point

            painter.drawLine(xx0, yy0, xx1, yy1)

        painter.end()

        return chart

    def draw_grid(self, painter, size, args):
        step = self.grid_step
        offset_x, offset_y = self.offset
        width, height = size
        x0, y0 = width / 2, height / 2

        painter.setPen(QPen(Qt.gray, 1))

        for i in range(int((x0 - offset_x) / step) + 1):
            xxs = [x0] if i == 0 else [x0 - i * step, x0 + i * step]

            for xx in xxs:
                x = -i if xx < x0 else i
                rect = QRect(xx - step / 2, height - offset_y + 8, step, 14)
                painter.drawLine(xx, offset_y, xx, height - offset_y)
                painter.drawText(rect, Qt.AlignHCenter, str(x))

        for i in range(int((y0 - offset_y) / step) + 1):
            yys = [y0] if i == 0 else [y0 - i * step, y0 + i * step]

            for yy in yys:
                y = -i if yy > y0 else i
                rect = QRect(0, yy - 7, offset_x - 8, 14)
                painter.drawLine(offset_x, yy, width - offset_x, yy)
                painter.drawText(rect, Qt.AlignRight, str(y))

    @staticmethod
    def create_func(a, b=None):
        def r(u):
            try:
                return a / (sqrt(cos(3 * radians(u))))
            except ValueError:
                return None

        return r
