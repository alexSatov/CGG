from typing import List, Tuple

from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from sympy import GeometryError
from sympy.geometry.polygon import Polygon

from chart import ChartArea, Chart, IGridPainter, Offset, \
    ChartBackgroundPainter
from options import OptionsBar


def parse_polygon(bar: OptionsBar, n: int) -> Polygon:
    points_arr: List[Tuple[int, int]] = []

    for i in range(n):
        x = int(bar.v_options[i].top.input.text())
        y = int(bar.v_options[i].bottom.input.text())
        points_arr.append((x, y))

    return Polygon(*points_arr)


def draw_polygon(polygon: Polygon, painter: QPainter, unit: int) -> None:
    for side in polygon.sides:
        p1 = QPoint(side.p1.x * unit, side.p1.y * unit)
        p2 = QPoint(side.p2.x * unit, side.p2.y * unit)

        painter.drawLine(p1, p2)


class Task4(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.unit: int = None
        self.width: int = None
        self.height: int = None
        self.pol1: Polygon = None
        self.pol2: Polygon = None
        self.pol1_n: int = None
        self.pol2_n: int = None
        self.v_layout = QVBoxLayout()
        self.main_opt_bar = OptionsBar(self)
        self.pol1_opt_bar = OptionsBar(self)
        self.pol2_opt_bar = OptionsBar(self)
        self.chart_area = ChartArea(self)
        self.init_ui()

    def init_ui(self) -> None:
        self.main_opt_bar \
            .with_int_options_v(400, 400, 'width', 'height', 10) \
            .with_int_options_v(4, 4, 'pol1_n', 'pol2_n', 3) \
            .with_int_option('unit', 40, 10, 100) \
            .with_button('Построить', self.build) \
            .with_button('Нарисовать', self.draw)

        self.v_layout.addWidget(self.main_opt_bar)
        self.v_layout.addWidget(self.pol1_opt_bar)
        self.v_layout.addWidget(self.pol2_opt_bar)
        self.v_layout.addWidget(self.chart_area)

        self.setLayout(self.v_layout)
        self.build()
        self.set_default()

    def parse_options(self) -> None:
        self.width = int(self.main_opt_bar.v_options[0].top.input.text())
        self.height = int(self.main_opt_bar.v_options[0].bottom.input.text())
        self.unit = int(self.main_opt_bar.options[0].input.text())

        self.pol1 = parse_polygon(self.pol1_opt_bar, self.pol1_n)
        self.pol2 = parse_polygon(self.pol2_opt_bar, self.pol2_n)

        print(self.pol1)
        print(self.pol2)

        if not (isinstance(self.pol1, Polygon) and
                isinstance(self.pol2, Polygon)):
            raise GeometryError()

    def draw(self) -> None:
        try:
            self.parse_options()
        except GeometryError:
            print('Incorrect polygon')
            return

        chart = Chart(self.width, self.height, pen_size=2)
        painter = chart.create_painter()

        draw_polygon(self.pol1, painter, self.unit)
        draw_polygon(self.pol2, painter, self.unit)

        back_painter = ChartBackgroundPainter(chart, revers=True)
        grid_painter = GridPainter(self, back_painter.offset, self.unit)
        back_painter.draw(grid_painter)

        self.chart_area.update(chart)

    def build(self) -> None:
        self.pol1_opt_bar.clear()
        self.pol2_opt_bar.clear()

        self.pol1_n = int(self.main_opt_bar.v_options[1].top.input.text())
        self.pol2_n = int(self.main_opt_bar.v_options[1].bottom.input.text())

        for i in range(self.pol1_n):
            self.pol1_opt_bar.with_int_options_v(
                0, 0, f'pol1_{i+1}_x', f'pol1_{i+1}_y', 0)

        for i in range(self.pol2_n):
            self.pol2_opt_bar.with_int_options_v(
                0, 0, f'pol2_{i+1}_x', f'pol2_{i+1}_y', 0)

    def set_default(self) -> None:
        self.pol1_opt_bar.v_options[0].top.input.setText('1')
        self.pol1_opt_bar.v_options[0].bottom.input.setText('1')
        self.pol1_opt_bar.v_options[1].top.input.setText('3')
        self.pol1_opt_bar.v_options[1].bottom.input.setText('1')
        self.pol1_opt_bar.v_options[2].top.input.setText('3')
        self.pol1_opt_bar.v_options[2].bottom.input.setText('4')
        self.pol1_opt_bar.v_options[3].top.input.setText('1')
        self.pol1_opt_bar.v_options[3].bottom.input.setText('4')

        self.pol2_opt_bar.v_options[0].top.input.setText('2')
        self.pol2_opt_bar.v_options[0].bottom.input.setText('2')
        self.pol2_opt_bar.v_options[1].top.input.setText('4')
        self.pol2_opt_bar.v_options[1].bottom.input.setText('2')
        self.pol2_opt_bar.v_options[2].top.input.setText('4')
        self.pol2_opt_bar.v_options[2].bottom.input.setText('3')
        self.pol2_opt_bar.v_options[3].top.input.setText('2')
        self.pol2_opt_bar.v_options[3].bottom.input.setText('3')


class GridPainter(IGridPainter):
    def __init__(self, task: Task4, offset: Offset, step: int):
        self.task = task
        self.offset = offset
        self.step = step

    def draw(self, painter: QPainter) -> None:
        step = self.step
        right_border = self.task.width + self.offset.x
        bottom_border = self.task.height + self.offset.y

        painter.setPen(QPen(Qt.gray, 1))

        for i in range(int(self.task.width / step) + 1):
            xx = step * i + self.offset.x
            rect = QRect(xx - step / 2, self.offset.y - 20, step, 14)

            painter.drawLine(xx, self.offset.y, xx, bottom_border)
            painter.drawText(rect, Qt.AlignHCenter, str(i))

        for i in range(int(self.task.height / step) + 1):
            yy = step * i + self.offset.y
            rect = QRect(0, yy - 7, self.offset.x - 8, 14)

            painter.drawLine(self.offset.x, yy, right_border, yy)
            painter.drawText(rect, Qt.AlignRight, str(i))
