from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QScrollArea, QLabel, QWidget


class Offset:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class IGridPainter:
    def draw(self, painter: QPainter, step: int = 40) -> None:
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
        self._painter: QPainter = None

    @property
    def painter(self) -> QPainter:
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

                if color == self.color:
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
                 h_axis: str = 'x', v_axis: str = 'y'):
        self.h_axis = h_axis
        self.v_axis = v_axis
        self.chart = chart
        self.offset = offset
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
