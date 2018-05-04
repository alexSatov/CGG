from math import inf, fabs

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QFont

from chart import Chart, ChartBackgroundPainter, IGridPainter, Offset
from task1 import Task1


Void = None


def sign(a: float) -> int:
    return (a > 0) - (a < 0)


def f(x: float) -> float:
    try:
        return 1 / x
    except ZeroDivisionError:
        return inf


def draw_bresenham_line(chart: Chart, x0: int, y0: int, x1: int, y1: int,
                        revert: bool = False) -> Void:
    if x0 > x1:
        draw_bresenham_line(chart, x1, y1, x0, y0)
        return

    dx, dy, y = fabs(x1 - x0), fabs(y1 - y0), y0

    if dy > dx:
        draw_bresenham_line(chart, y0, x0, y1, x1, True)
        return

    de, e = dy, 0
    y_dir = sign(y1 - y0)

    for x in range(x0, x1):
        chart.image.setPixelColor(y, x, chart.color) if revert else \
            chart.image.setPixelColor(x, y, chart.color)
        e += de

        if 2 * e >= de:
            y += y_dir
            e -= dx


class Task3(Task1):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.f = f
        self.step: int = None
        self.lim_min_y: float = None
        self.lim_max_y: float = None

    def init_ui(self) -> Void:
        self.options_bar \
            .with_area() \
            .with_int_options_v(0, 10) \
            .with_int_option('lim_min_y', 0) \
            .with_int_option('lim_max_y', 10) \
            .with_int_option('step', 10, 10, 100) \
            .with_button('Нарисовать', self.draw_chart)

    def parse_input(self) -> Void:
        ox = int(self.options_bar.area.left_top.x.input.text())
        oy = int(self.options_bar.area.left_top.y.input.text())
        max_x = int(self.options_bar.area.right_bottom.x.input.text())
        max_y = int(self.options_bar.area.right_bottom.y.input.text())
        self.alpha = int(self.options_bar.v_options[0].top.input.text())
        self.beta = int(self.options_bar.v_options[0].bottom.input.text())
        self.lim_min_y = int(self.options_bar.options[0].input.text())
        self.lim_max_y = int(self.options_bar.options[1].input.text())
        self.step = int(self.options_bar.options[2].input.text())

        self.width = (max_x - ox) // self.step
        self.height = (max_y - oy) // self.step

    def create_chart(self) -> Chart:
        self.calculate()
        self.min_y = self.min_y if self.min_y >= self.lim_min_y \
            else self.lim_min_y
        self.max_y = self.max_y if self.max_y <= self.lim_max_y \
            else self.lim_max_y

        chart = Chart(self.width, self.height)

        dy = self.max_y - self.min_y if self.max_y - self.min_y >= 0 else 0
        y = self.f_x_y[self.alpha]
        yy = (self.max_y - y) * self.height / dy if y != inf and dy != 0 \
            else inf
        xx0, yy0 = 0, yy

        for xx in range(1, self.width):
            x = self.f_xx_x[xx]
            y = self.f_x_y[x]
            yy = (self.max_y - y) * self.height / dy if y != inf and dy != 0 \
                else inf

            if inf not in (yy, yy0) and (yy > 0 or yy0 > 0):
                draw_bresenham_line(chart, xx0, round(yy0), xx, round(yy))

            xx0, yy0 = xx, yy

        chart = self.zoom(chart)
        back_painter = ChartBackgroundPainter(chart)
        grid_painter = GridPainter(self, back_painter.offset, self.step)
        back_painter.draw(grid_painter)

        return chart

    def zoom(self, chart: Chart) -> Chart:
        unit = self.step
        self.width, self.height = chart.width * unit, chart.height * unit
        copy = Chart(self.width, self.height)
        painter = QPainter(copy.image)

        for x in range(chart.width):
            for y in range(chart.height):
                color = chart.image.pixelColor(x, y)
                rect = QRect(x * unit, y * unit, unit, unit)
                painter.setBrush(color)
                painter.drawRect(rect)

        painter.end()

        return copy


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
            x = self.f_xx_x[(xx - self.offset.x) // self.step]
            rect = QRect(xx - 40 / 2, bottom_border + 8, 40, 14)
            painter.drawLine(xx, self.offset.y, xx, bottom_border)

            if xx % 40 < 10:
                painter.drawText(rect, Qt.AlignHCenter, '%.2f' % x)

        for yy in range(self.offset.y, bottom_border, self.step):
            yy = self.height + self.offset.y - yy
            back_yy = yy + self.offset.y
            rect = QRect(0, back_yy - 7, self.offset.x - 8, 14)
            y = (yy * dy / self.height) + self.max_y if not is_constant else \
                (self.height / 2 - yy) + self.max_y
            painter.drawLine(self.offset.x, back_yy, right_border, back_yy)

            if yy % 40 < 10:
                painter.drawText(rect, Qt.AlignRight, '%.2f' % y)
