from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QFont
from PyQt5.QtWidgets import QScrollArea, QLabel, QWidget


class Offset:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class IGridPainter:
    def draw(self, painter: QPainter) -> None:
        raise NotImplementedError()


class Chart:
    def __init__(self, width: int, height: int, color: QColor = Qt.blue,
                 pen_size: int = 3, image_format: int = QImage.Format_ARGB32):
        self.width = width
        self.height = height
        self.color = color
        self.colors = [color]
        self.pen_size = pen_size
        self.image_format = image_format
        self.image = QImage(width, height, image_format)
        self._painter: QPainter = None

    def create_painter(self) -> QPainter:
        self._painter = QPainter(self.image)
        self._painter.setPen(QPen(self.color, self.pen_size))

        return self._painter

    def add_background(self, background: QImage, offset: Offset) -> None:
        if self._painter:
            self._painter.end()

        chart = self.image

        for x in range(self.width):
            for y in range(self.height):
                color = chart.pixelColor(x, y)

                if color in self.colors:
                    background.setPixelColor(x + offset.x, y + offset.y, color)

        self.image = background


class ChartArea(QScrollArea):
    def __init__(self, task_widget: QWidget):
        super().__init__(task_widget)
        self.task_widget = task_widget
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setWidgetResizable(True)
        self.setWidget(self.image_label)

    def update(self, chart: Chart) -> None:
        self.image_label.setPixmap(QPixmap(chart.image))


class ChartBackgroundPainter:
    def __init__(self, chart: Chart, offset: Offset = Offset(80, 40),
                 h_axis: str = 'x', v_axis: str = 'y', revers: bool = False):
        self.chart = chart
        self.offset = offset
        self.h_axis = h_axis
        self.v_axis = v_axis
        self.reversed = revers
        self.size = QSize(chart.width + offset.x * 2,
                          chart.height + offset.y * 2)

    def draw(self, grid_painter: IGridPainter) -> None:
        background = QImage(self.size, self.chart.image_format)
        background.fill(Qt.white)
        painter = QPainter(background)

        grid_painter.draw(painter)
        self.draw_axis(painter)

        painter.end()

        self.chart.add_background(background, self.offset)

    def draw_axis(self, painter: QPainter) -> None:
        width, height = self.size.width(), self.size.height()
        ox_y = self.offset.y if self.reversed else height - self.offset.y
        oy_x = self.offset.x

        painter.setPen(QPen(Qt.black, 2))
        painter.setFont(QFont('Arial', 10, 75))

        if self.reversed:
            painter.drawLine(oy_x, ox_y, width, ox_y)
            painter.drawLine(width, ox_y, width - 10, ox_y - 4)
            painter.drawLine(width, ox_y, width - 10, ox_y + 4)
            painter.drawText(width - 20, ox_y - 10, self.h_axis)

            painter.drawLine(oy_x, self.offset.y, oy_x, height)
            painter.drawLine(oy_x, height, oy_x - 4, height - 10)
            painter.drawLine(oy_x, height, oy_x + 4, height - 10)
            painter.drawText(oy_x - 20, height - 15, self.v_axis)
        else:
            painter.drawLine(oy_x, ox_y, width, ox_y)
            painter.drawLine(width, ox_y, width - 10, ox_y - 4)
            painter.drawLine(width, ox_y, width - 10, ox_y + 4)
            painter.drawText(width - 20, ox_y + 20, self.h_axis)

            painter.drawLine(oy_x, ox_y, oy_x, 0)
            painter.drawLine(oy_x, 0, oy_x - 4, 10)
            painter.drawLine(oy_x, 0, oy_x + 4, 10)
            painter.drawText(oy_x + 10, 15, self.v_axis)
