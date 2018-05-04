from math import fabs
from typing import List, Tuple

from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from sympy import GeometryError
from sympy.geometry.polygon import Polygon
from sympy.geometry.point import Point2D
from sympy.geometry.line import Segment2D

from chart import ChartArea, Chart, IGridPainter, Offset, \
    ChartBackgroundPainter
from options import OptionsBar


Point = Tuple[float, float]
Line = Tuple[Point, Point]
Chain = List[Point]


def parse_polygon(bar: OptionsBar, n: int) -> Polygon:
    points_arr: List[Tuple[int, int]] = []

    for i in range(n):
        x = int(bar.v_options[i].top.input.text())
        y = int(bar.v_options[i].bottom.input.text())
        points_arr.append((x, y))

    return Polygon(*points_arr)


def is_inside(this: Polygon, other: Polygon) -> bool:
    for point in this.vertices:
        if not other.encloses_point(point):
            return False

    return True


def to_chain(polygon: Polygon) -> Chain:
    vertices: List[Point2D] = polygon.vertices
    first = (vertices[0].x, vertices[0].y)
    chain = list(map(lambda p: (p.x, p.y), polygon.vertices))
    chain.append(first)
    return chain


def get_line_with_point(polygon: Polygon, point: Point) -> Line:
    for side in polygon.sides:
        if len(side.intersection(point)) != 0:
            return (side.p1.x, side.p1.y), (side.p2.x, side.p2.y)


def get_insert_pos(chain: Chain, line: Line, point: Point) -> int:
    lp = chain.index(line[0]) if chain.count(line[0]) == 1 else None
    rp = chain.index(line[1]) if chain.count(line[1]) == 1 else None

    if not lp:
        lp = 0 if rp < len(chain) - 1 - rp else len(chain) - 1

    if not rp:
        rp = 0 if lp < len(chain) - 1 - lp else len(chain) - 1

    if fabs(lp - rp) == 1:
        return max(lp, rp)

    if lp < rp:
        for i in range(lp + 1, rp):
            if Point2D(chain[lp]).distance(point) < \
                    Point2D(point).distance(chain[i]):
                return i

    for i in range(lp - 1, rp, -1):
        if Point2D(chain[lp]).distance(point) < \
                Point2D(point).distance(chain[i]):
            return i + 1


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

        self.pol2_opt_bar.v_options[0].top.input.setText('0')
        self.pol2_opt_bar.v_options[0].bottom.input.setText('2')
        self.pol2_opt_bar.v_options[1].top.input.setText('4')
        self.pol2_opt_bar.v_options[1].bottom.input.setText('2')
        self.pol2_opt_bar.v_options[2].top.input.setText('4')
        self.pol2_opt_bar.v_options[2].bottom.input.setText('3')
        self.pol2_opt_bar.v_options[3].top.input.setText('0')
        self.pol2_opt_bar.v_options[3].bottom.input.setText('3')

    def draw(self) -> None:
        try:
            self.parse_options()
        except GeometryError:
            print('Incorrect polygon')
            return

        chart = Chart(self.width, self.height, pen_size=2)
        chart.colors.append(Qt.red)

        painter = chart.create_painter()
        inside, outside = self.get_symmetric_difference()

        for chain in inside:
            self.draw_chain(chain, painter)

        painter.setPen(QPen(Qt.red, 2))

        for chain in outside:
            self.draw_chain(chain, painter)

        back_painter = ChartBackgroundPainter(chart, revers=True)
        grid_painter = GridPainter(self, back_painter.offset, self.unit)
        back_painter.draw(grid_painter)

        self.chart_area.update(chart)

    def get_symmetric_difference(self) -> Tuple[List[Chain], List[Chain]]:
        c1, c2 = to_chain(self.pol1), to_chain(self.pol2)

        if is_inside(self.pol1, self.pol2):
            return [c1], [c2]
        if is_inside(self.pol2, self.pol1):
            return [c2], [c1]

        ps_in = set()
        ps_out = set()
        cur_point = c1[0]
        to_inside = not self.pol2.encloses_point(cur_point)
        full_c1, full_c2 = [cur_point], c2

        for point in c1[1:]:
            line = Segment2D(cur_point, point)
            intersection = sorted(self.pol2.intersection(line),
                                  key=lambda p: p.distance(cur_point))

            if len(intersection) == 0:
                cur_point = point
                full_c1.append(point)
                continue

            for i in range(len(intersection)):
                i_point = (intersection[i].x / 1.0, intersection[i].y / 1.0)
                i_line = get_line_with_point(self.pol2, i_point)
                pos = get_insert_pos(c2, i_line, i_point)
                full_c2.insert(pos, i_point)
                full_c1.append(i_point)

                if to_inside:
                    if i / 2 == 0:
                        ps_in.add(i_point)
                    else:
                        ps_out.add(i_point)
                else:
                    if i / 2 == 0:
                        ps_out.add(i_point)
                    else:
                        ps_in.add(i_point)

            cur_point = point
            to_inside = not self.pol2.encloses_point(cur_point)
            full_c1.append(point)

        if len(ps_in) == 0:
            return [], [c1, c2]

        inside_chains, outside_chains = [], []
        c_full_c1, c_full_c2 = full_c1 + full_c1[1:], full_c2 + full_c2[1:]

        for p_in in ps_in:
            inside_chain = [p_in]
            outside_chain = [p_in]
            pos1 = full_c1.index(p_in)
            pos2 = full_c2.index(p_in)

            for i in range(pos1 + 1, len(c_full_c1)):
                point = c_full_c1[i]
                inside_chain.append(point)

                if point in ps_out:
                    pos = full_c2.index(point)

                    for j in range(pos + 1, len(c_full_c2)):
                        point = c_full_c2[j]
                        inside_chain.append(point)

                        if point in ps_in:
                            break
                    break

            for i in range(pos2 + 1, len(c_full_c2)):
                point = c_full_c2[i]
                outside_chain.append(point)

                if point in ps_out:
                    break

            inside_chains.append(inside_chain)
            outside_chains.append(outside_chain)

        for p_out in ps_out:
            outside_chain = [p_out]
            pos = full_c1.index(p_out)

            for i in range(pos + 1, len(c_full_c1)):
                point = c_full_c1[i]
                outside_chain.append(point)

                if point in ps_in:
                    outside_chains.append(outside_chain)
                    break

        return inside_chains, outside_chains

    def draw_polygon(self, polygon: Polygon, painter: QPainter) -> None:
        for side in polygon.sides:
            p1 = QPoint(side.p1.x * self.unit, side.p1.y * self.unit)
            p2 = QPoint(side.p2.x * self.unit, side.p2.y * self.unit)

            painter.drawLine(p1, p2)

    def draw_chain(self, chain: Chain, painter: QPainter) -> None:
        if len(chain) < 2:
            return

        cur_point = QPoint(chain[0][0] * self.unit, chain[0][1] * self.unit)

        for point in chain[1:]:
            move_point = QPoint(point[0] * self.unit, point[1] * self.unit)
            painter.drawLine(cur_point, move_point)
            cur_point = move_point


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
