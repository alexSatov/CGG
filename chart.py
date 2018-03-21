from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QScrollArea, QLabel


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
