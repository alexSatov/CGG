from math import inf
from typing import Dict

from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QFont

from chart import Chart, IGridPainter, Offset, ChartBackgroundPainter
from task import Task, Func

Cache = Dict[float, float]


class Task1(Task):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.f_xx_x: Cache = None
        self.f_x_y: Cache = None
        self.min_y: float = None
        self.max_y: float = None
        self.init_ui()

    def init_ui(self) -> None:
        self.options_bar \
            .with_area() \
            .with_int_options_v() \
            .with_int_option('a', 1) \
            .with_int_option('b', 0) \
            .with_button('Нарисовать', self.draw_chart) \
            .with_image('images\\task1.png')

    def parse_input(self) -> None:
        ox = int(self.options_bar.area.left_top.x.input.text())
        oy = int(self.options_bar.area.left_top.y.input.text())
        max_x = int(self.options_bar.area.right_bottom.x.input.text())
        max_y = int(self.options_bar.area.right_bottom.y.input.text())
        self.alpha = int(self.options_bar.v_options[0].top.input.text())
        self.beta = int(self.options_bar.v_options[0].bottom.input.text())
        a = int(self.options_bar.options[0].input.text())
        b = int(self.options_bar.options[1].input.text())

        self.width = max_x - ox
        self.height = max_y - oy
        self.f = Task1.create_func(a, b)

    def create_chart(self) -> Chart:
        self.calculate()

        chart = Chart(self.width, self.height)
        painter = chart.create_painter()

        if self.min_y == self.max_y:
            self.draw_constant_chart(painter)
            painter.end()
            self.add_background(chart)

            return chart

        dy = self.max_y - self.min_y
        y = self.f_x_y[self.alpha]
        yy = (self.max_y - y) * self.height / dy
        current_point = QPoint(0, yy)

        for xx in range(1, self.width):
            x = self.f_xx_x[xx]
            y = self.f_x_y[x]
            yy = (self.max_y - y) * self.height / dy if y != inf else inf
            move_point = QPoint(xx, round(yy)) if yy != inf else None

            if None not in (current_point, move_point):
                painter.drawLine(current_point, move_point)

            current_point = move_point

        back_painter = ChartBackgroundPainter(chart)
        grid_painter = GridPainter(self, back_painter.offset)
        back_painter.draw(grid_painter)

        return chart

    def calculate(self) -> None:
        self.f_xx_x, self.f_x_y = {}, {}
        self.min_y, self.max_y = inf, -inf

        for xx in range(0, self.width):
            x = self.alpha + xx * (self.beta - self.alpha) / self.width
            y = self.f(x)
            self.f_xx_x[xx] = x
            self.f_x_y[x] = y

            if y == inf:
                continue
            if y < self.min_y:
                self.min_y = y
            if y > self.max_y:
                self.max_y = y

    def draw_constant_chart(self, painter: QPainter) -> None:
        yy = round(self.height / 2)

        painter.drawLine(0, yy, self.width, yy)
        painter.setPen(QPen(Qt.white, 2))

        for x, y in self.f_x_y.items():
            if y != inf:
                continue

            for xx in self.f_xx_x.keys():
                if x == self.f_xx_x[xx]:
                    painter.drawPoint(xx, yy)

    @staticmethod
    def create_func(a: int, b: int) -> Func:
        def f(x: float) -> float:
            try:
                return ((a + x) / (b - x)) ** 4
            except ZeroDivisionError:
                return inf

        return f


class GridPainter(IGridPainter):
    def __init__(self, task: Task1, offset: Offset, step: int = 40):
        self.min_y = task.min_y
        self.max_y = task.max_y
        self.width = task.width
        self.height = task.height
        self.f_xx_x = task.f_xx_x
        self.offset = offset
        self.step = step

    def draw(self, painter: QPainter) -> None:
        dy = self.min_y - self.max_y
        is_constant = self.min_y == self.max_y
        right_border = self.width + self.offset.x
        bottom_border = self.height + self.offset.y

        painter.setPen(QPen(Qt.gray, 1))
        painter.setFont(QFont('Arial', 8))

        for xx in range(self.offset.x, right_border, self.step):
            x = self.f_xx_x[xx - self.offset.x]
            rect = QRect(xx - self.step / 2, bottom_border + 8, self.step, 14)
            painter.drawLine(xx, self.offset.y, xx, bottom_border)
            painter.drawText(rect, Qt.AlignHCenter, '%.2f' % x)

        for yy in range(self.offset.y, bottom_border, self.step):
            yy = self.height + self.offset.y - yy
            back_yy = yy + self.offset.y
            rect = QRect(0, back_yy - 7, self.offset.x - 8, 14)
            y = (yy * dy / self.height) + self.max_y if not is_constant else \
                (self.height / 2 - yy) + self.max_y
            painter.drawLine(self.offset.x, back_yy, right_border, back_yy)
            painter.drawText(rect, Qt.AlignRight, '%.2f' % y)
