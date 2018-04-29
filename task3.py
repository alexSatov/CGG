from math import inf, fabs

from chart import Chart, ChartBackgroundPainter
from task1 import Task1, GridPainter


def sign(a: float) -> int:
    return (a > 0) - (a < 0)


def f(x: float) -> float:
    try:
        return 1 / x
    except ZeroDivisionError:
        return inf


def draw_bresenham_line(chart: Chart, x0: int, y0: int, x1: int, y1: int,
                        revert: bool = False) -> None:
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
        self.lim_min_y: float = None
        self.lim_max_y: float = None

    def init_ui(self) -> None:
        self.options_bar \
            .with_area() \
            .with_int_options_v(-10, 10) \
            .with_int_option('lim_min_y', -10) \
            .with_int_option('lim_max_y', 10) \
            .with_button('Нарисовать', self.draw_chart)

    def parse_input(self) -> None:
        ox = int(self.options_bar.area.left_top.x.input.text())
        oy = int(self.options_bar.area.left_top.y.input.text())
        max_x = int(self.options_bar.area.right_bottom.x.input.text())
        max_y = int(self.options_bar.area.right_bottom.y.input.text())
        self.alpha = int(self.options_bar.v_options[0].top.input.text())
        self.beta = int(self.options_bar.v_options[0].bottom.input.text())
        self.lim_min_y = int(self.options_bar.options[0].input.text())
        self.lim_max_y = int(self.options_bar.options[1].input.text())

        self.width = max_x - ox
        self.height = max_y - oy

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

        back_painter = ChartBackgroundPainter(chart)
        grid_painter = GridPainter(self, back_painter.offset)
        back_painter.draw(grid_painter)

        return chart
