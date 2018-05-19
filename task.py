from typing import Callable

from PyQt5.QtWidgets import QWidget, QVBoxLayout

from chart import ChartArea, Chart
from options import OptionsBar

Func = Callable[[float], float]


class Task(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.width = 0
        self.height = 0
        self.alpha = 0
        self.beta = 0
        self.f: Callable = Func
        self.chart_area = ChartArea(self)
        self.options_bar = OptionsBar(self)
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.options_bar)
        self.v_layout.addWidget(self.chart_area)
        self.setLayout(self.v_layout)

    def draw_chart(self) -> None:
        self.parse_input()

        if not self.valid():
            return

        chart = self.create_chart()

        self.chart_area.update(chart)

    def valid(self) -> bool:
        return self.width > 0 and self.height > 0 and self.beta > self.alpha

    def create_chart(self) -> Chart:
        raise NotImplementedError()
