from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QScrollArea, QLabel, QWidget


class Offset:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class IGridPainter:
    def draw(self, painter: QPainter, step: int = 40):
        raise NotImplementedError()


class Chart:
    def __init__(self, width, height, color: QColor = Qt.blue,
                 pen_size: int = 3, image_format: int = QImage.Format_ARGB32):
        self.width = width
        self.height = height
        self.color = color
        self.pen_size = pen_size
        self.image_format = image_format
        self.image = QImage(width, height, image_format)

    def get_painter(self) -> QPainter:
        painter = QPainter(self.image)
        painter.setPen(QPen(self.color, self.pen_size))

        return painter

    def with_background(self, background: QImage) -> None:
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


class ChartBackground:
    def __init__(self, chart: Chart, offset: Offset = Offset(80, 40),
                 h_axis: str = 'x', v_axis: str = 'y'):
        self.h_axis = h_axis
        self.v_axis = v_axis
        self.chart = chart
        self.offset = offset
        self.size = QSize(chart.width + offset.x * 2,
                          chart.height + offset.y * 2)

        self.image = QImage(self.size, self.chart.image_format)

    def update(self, grid_painter: IGridPainter) -> None:
        painter = QPainter(self.image)

        self.image.fill(Qt.white)
        grid_painter.draw(painter)
        self.draw_axis(painter)
        self.insert_chart()

        painter.end()

    def draw_axis(self, painter: QPainter) -> None:
        width, height = self.size.width(), self.size.height()
        oxy, oyx = height - self.offset.y, self.offset.x

        painter.setPen(QPen(Qt.black, 2))
        painter.setFont(QFont('Arial', 10, 75))

        painter.drawLine(self.offset.x, oxy, width, oxy)
        painter.drawLine(width, oxy, width - 10, oxy - 4)
        painter.drawLine(width, oxy, width - 10, oxy + 4)
        painter.drawText(width - 20, height - self.offset.y + 20, self.h_axis)

        painter.drawLine(oyx, height - self.offset.y, oyx, 0)
        painter.drawLine(oyx, 0, oyx - 4, 10)
        painter.drawLine(oyx, 0, oyx + 4, 10)
        painter.drawText(self.offset.x + 10, 15, self.v_axis)

    def insert_chart(self) -> None:
        for x in range(self.chart.width):
            for y in range(self.chart.height):
                color = self.chart.image.pixelColor(x, y)

                if color == self.chart.color:
                    self.image.setPixelColor(x + self.offset.x,
                                             y + self.offset.y, color)
