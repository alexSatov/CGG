from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QScrollArea, QLabel


def insert(chart, back, x1, y1):
    offset_x = -x1 if x1 < 0 else 0
    offset_y = -y1 if y1 < 0 else 0
    x2 = x1 + chart.width() - 1
    y2 = y1 + chart.height() - 1
    width = chart.width() if x2 < back.width() else back.width() - x1
    height = chart.height() if y2 < back.height() else back.height() - y1

    for x in range(width - offset_x):
        for y in range(height - offset_y):
            color = chart.pixelColor(x + offset_x, y + offset_y)

            if color != Qt.blue:
                continue

            back.setPixelColor(x + x1 + offset_x, y + y1 + offset_y, color)


class ChartArea(QScrollArea):
    def __init__(self, task_widget):
        super().__init__(task_widget)
        self.task_widget = task_widget
        self.image = None
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setWidgetResizable(True)
        self.setWidget(self.image_label)

    def update(self):
        self.image_label.setPixmap(QPixmap(self.image))
