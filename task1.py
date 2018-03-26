from math import inf

from options import OptionsBar
from chartArea import ChartArea

from PyQt5.QtGui import QImage, QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class Task1(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.offset = 80, 40
        self.grid_step = 40
        self.chart_area = ChartArea(self)
        self.options_bar = OptionsBar(self)
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.options_bar)
        self.v_layout.addWidget(self.chart_area)
        self.init_ui()

    def init_ui(self):
        self.options_bar \
            .with_area() \
            .with_interval() \
            .with_int_option('a', 1) \
            .with_int_option('b', 0) \
            .with_button('Нарисовать', self.draw_chart) \
            .with_image('images\\task1.png')

        self.setLayout(self.v_layout)

    def draw_chart(self):
        args = self.parse_input()

        if not self.valid(args):
            return

        chart = self.create_chart(args)

        self.chart_area.set_chart(chart)

    def parse_input(self):
        ox = int(self.options_bar.area.left_top.x.input.text())
        oy = int(self.options_bar.area.left_top.y.input.text())
        maxx = int(self.options_bar.area.right_bottom.x.input.text())
        maxy = int(self.options_bar.area.right_bottom.y.input.text())
        alpha = int(self.options_bar.interval.alpha.input.text())
        beta = int(self.options_bar.interval.beta.input.text())
        a = int(self.options_bar.options[0].input.text())
        b = int(self.options_bar.options[1].input.text())
        f = self.create_func(a, b)

        return maxx - ox, maxy - oy, alpha, beta, f

    def create_chart(self, args):
        width, height, a, b, f = args
        ymin, ymax, fx, fy = self.calculate(f, width, a, b)
        chart = self.get_chart(a, ymin, ymax, width, height, fx, fy)
        chart = self.add_axis_and_grid(chart, fx, ymin, ymax, 'X', 'Y')

        return chart

    def get_chart(self, *args):
        a, ymin, ymax, maxx, maxy, fx, fy = args
        chart = QImage(maxx, maxy, QImage.Format_ARGB32)
        painter = QPainter(chart)
        painter.setPen(QPen(Qt.blue, 3))

        if ymax == ymin:
            self.draw_constant_chart(painter, maxx, maxy, fx, fy)
            painter.end()

            return chart

        yy = (fy[a] - ymax) * maxy / (ymin - ymax)
        current_point = QPoint(0, yy)

        for xx in range(1, maxx):
            x = fx[xx]
            y = fy[x]
            yy = (y - ymax) * maxy / (ymin - ymax) if y != inf else inf
            move_point = QPoint(xx, round(yy)) if yy != inf else None

            if None not in (current_point, move_point):
                painter.drawLine(current_point, move_point)

            current_point = move_point

        painter.end()

        return chart

    def add_axis_and_grid(self, chart, *args):
        offset_x, offset_y = self.offset
        size = chart.width() + offset_x * 2, chart.height() + offset_y * 2

        background = QImage(size[0], size[1], QImage.Format_ARGB32)
        background.fill(Qt.white)

        painter = QPainter(background)

        self.draw_grid(painter, size, args)
        self.draw_axis(painter, size, args)

        painter.end()

        self.insert(chart, background)

        return background

    def draw_grid(self, painter, size, args):
        step = self.grid_step
        width, height = size
        offset_x, offset_y = self.offset
        fx, ymin, ymax, _, _ = args
        chart_height = height - offset_y * 2

        painter.setPen(QPen(Qt.gray, 1))
        painter.setFont(QFont('Arial', 8))

        for xx in range(offset_x, width - offset_x, step):
            rect = QRect(xx - step / 2, height - offset_y + 8, step, 14)
            painter.drawLine(xx, offset_y, xx, height - offset_y)
            painter.drawText(rect, Qt.AlignHCenter, '%.2f' % fx[xx - offset_x])

        for yy in range(offset_y, height - offset_y, step):
            yy = height - yy
            rect = QRect(0, yy - 7, offset_x - 8, 14)
            y = ((yy - offset_y) * (ymin - ymax) / chart_height) + ymax if \
                ymin != ymax else (chart_height / 2 - yy + offset_y) + ymax
            painter.drawLine(offset_x, yy, width - offset_x, yy)
            painter.drawText(rect, Qt.AlignRight, '%.2f' % y)

    def draw_axis(self, painter, size, args):
        width, height = size
        offset_x, offset_y = self.offset
        h_name, v_name = args[-2], args[-1]
        oxy, oyx = height - offset_y, offset_x

        painter.setPen(QPen(Qt.black, 2))
        painter.setFont(QFont('Arial', 10, 75))

        painter.drawLine(offset_x, oxy, width, oxy)
        painter.drawLine(width, oxy, width - 10, oxy - 4)
        painter.drawLine(width, oxy, width - 10, oxy + 4)
        painter.drawText(width - 20, height - offset_y + 20, h_name)

        painter.drawLine(oyx, height - offset_y, oyx, 0)
        painter.drawLine(oyx, 0, oyx - 4, 10)
        painter.drawLine(oyx, 0, oyx + 4, 10)
        painter.drawText(offset_x + 10, 15, v_name)

    def insert(self, chart, back):
        offset_x, offset_y = self.offset
        width, height = chart.width(), chart.height()

        for x in range(width):
            for y in range(height):
                color = chart.pixelColor(x, y)

                if color == Qt.blue:
                    back.setPixelColor(x + offset_x, y + offset_y, color)

    @staticmethod
    def create_func(a, b):
        def f(x):
            try:
                return ((a + x) / (b - x)) ** 4
            except ZeroDivisionError:
                return inf

        return f

    @staticmethod
    def valid(args):
        width, height, a, b, _ = args

        return width > 0 and height > 0 and b > a

    @staticmethod
    def calculate(f, maxx, a, b):
        ymin = inf
        ymax = -inf
        fx, fy = {}, {}

        for xx in range(0, maxx):
            x = a + xx * (b - a) / maxx
            y = f(x)
            fx[xx] = x
            fy[x] = y

            if y == inf:
                continue
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y

        return ymin, ymax, fx, fy

    @staticmethod
    def draw_constant_chart(painter, maxx, maxy, fx, fy):
        yy = round(maxy / 2)

        painter.drawLine(0, yy, maxx, yy)
        painter.setPen(QPen(Qt.white, 2))

        for x, y in fy.items():
            if y == inf:
                for xx in fx.keys():
                    if x == fx[xx]:
                        painter.drawPoint(xx, yy)
