from math import radians as rad
from math import sqrt, cos, sin, fabs

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen

from chart import Chart, IGridPainter, Offset, ChartBackgroundPainter
from task import Task, Func


class PixelPoint:
    def __init__(self, x, y, unit):
        self.x = round(x * unit)
        self.y = round(y * unit)

    def get_distance(self, other: 'PixelPoint') -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Task2(Task):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.init_ui()

    def init_ui(self) -> None:
        self.options_bar \
            .with_area() \
            .with_int_options_v(0, 360) \
            .with_int_option('a', 1) \
            .with_button('Нарисовать', self.draw_chart) \
            .with_image('images\\task2.png')

    def parse_input(self) -> None:
        ox = int(self.options_bar.area.left_top.x.input.text())
        oy = int(self.options_bar.area.left_top.y.input.text())
        max_x = int(self.options_bar.area.right_bottom.x.input.text())
        max_y = int(self.options_bar.area.right_bottom.y.input.text())
        self.alpha = int(self.options_bar.v_options[0].top.input.text())
        self.beta = int(self.options_bar.v_options[0].bottom.input.text())
        a = int(self.options_bar.options[0].input.text())

        self.width = max_x - ox
        self.height = max_y - oy
        self.f = Task2.create_func(a)

    def create_chart(self) -> Chart:
        u0, u1, r = self.alpha, self.beta, self.f
        x0, y0, unit = self.width // 2, self.height // 2, 40
        chart = Chart(self.width, self.height)
        painter = chart.create_painter()
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

        back_painter = ChartBackgroundPainter(chart, h_axis='r', v_axis='φ')
        grid_painter = GridPainter(self, back_painter.offset)
        back_painter.draw(grid_painter)

        return chart

    @staticmethod
    def create_func(a: int) -> Func:
        def r(u):
            try:
                return a / (sqrt(cos(3 * rad(u))))
            except ValueError:
                return None

        return r


class GridPainter(IGridPainter):
    def __init__(self, task: Task2, offset: Offset):
        self.task = task
        self.offset = offset
        self.step = 40

    def draw(self, painter: QPainter, step: int = 40) -> None:
        width, height = self.task.width + self.offset.x * 2, \
                        self.task.height + self.offset.y * 2
        x0, y0, step = width / 2, height / 2, self.step
        bottom_border = height - self.offset.y

        painter.setPen(QPen(Qt.gray, 1))

        for i in range(int((x0 - self.offset.x) / step) + 1):
            xxs = [x0] if i == 0 else [x0 - i * step, x0 + i * step]

            for xx in xxs:
                x = -i if xx < x0 else i
                rect = QRect(xx - step / 2, bottom_border + 8, step, 14)
                painter.drawLine(xx, self.offset.y, xx, bottom_border)
                painter.drawText(rect, Qt.AlignHCenter, str(x))

        for i in range(int((y0 - self.offset.y) / step) + 1):
            yys = [y0] if i == 0 else [y0 - i * step, y0 + i * step]

            for yy in yys:
                y = -i if yy > y0 else i
                rect = QRect(0, yy - 7, self.offset.x - 8, 14)
                painter.drawLine(self.offset.x, yy, width - self.offset.x, yy)
                painter.drawText(rect, Qt.AlignRight, str(y))
