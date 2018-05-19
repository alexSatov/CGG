from math import sin, radians as rad

from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPen, QPainter, QBrush

from chart import Chart
from task import Task


class Task6(Task):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.h = 0
        self.r = 0
        self.skew = 0
        self.init_ui()

    def init_ui(self) -> None:
        self.options_bar \
            .with_int_options_v(800, 600, 'width', 'height') \
            .with_int_options_v(260, 80, 'h', 'r') \
            .with_int_option('skew', 30) \
            .with_button('Нарисовать', self.draw_chart)

    def parse_input(self) -> None:
        self.width = int(self.options_bar.v_options[0].top.input.text())
        self.height = int(self.options_bar.v_options[0].bottom.input.text())
        self.h = int(self.options_bar.v_options[1].top.input.text())
        self.r = int(self.options_bar.v_options[1].bottom.input.text())
        self.skew = int(self.options_bar.options[0].input.text())

    def valid(self) -> bool:
        return self.width > 0 and self.height > 0 and self.h > 0 and self.r > 0 and \
            0 < self.skew < 180

    def create_chart(self) -> Chart:
        o = QPoint(self.width // 2, self.height // 2)
        h, r, d = self.h, self.r, self.r * 2
        dh = int(d * sin(rad(self.skew)))

        rect = QRect(o.x() - r, o.y() - h // 2, d, h)
        bottom_ellipse = QRect(o.x() - r, o.y() + h // 2 - dh // 2, d, dh)
        top_ellipse = QRect(o.x() - r, o.y() - h // 2 - dh // 2, d, dh)

        chart = Chart(self.width, self.height, Qt.black, 2)
        chart.image.fill(Qt.white)

        painter = QPainter(chart.image)

        painter.setPen(QPen(Qt.black, 5))
        painter.drawRect(rect)
        painter.drawEllipse(bottom_ellipse)
        painter.setPen(QPen(Qt.blue, 0))
        painter.setBrush(QBrush(Qt.blue))
        painter.drawRect(rect)
        painter.drawEllipse(bottom_ellipse)
        painter.setPen(QPen(Qt.black, 3))
        painter.drawEllipse(top_ellipse)

        painter.end()

        return chart
