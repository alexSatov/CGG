from typing import Callable

from chart import ChartArea, Chart
from options import OptionsBar

from PyQt5.QtWidgets import QWidget, QVBoxLayout


Func = Callable[[float], float]


class Task(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.width: int = None
        self.height: int = None
        self.alpha: int = None
        self.beta: int = None
        self.f: Callable = Func
        self.chart_area = ChartArea(self)
        self.options_bar = OptionsBar(self)
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.options_bar)
        self.v_layout.addWidget(self.chart_area)
        self.setLayout(self.v_layout)

    def draw_chart(self) -> None:
        self.parse_input()

        if not self.validate():
            return

        chart = self.create_chart()

        self.chart_area.update(chart)

    def validate(self) -> bool:
        return self.width > 0 and self.height > 0 and self.beta > self.alpha

    def create_chart(self) -> Chart:
        raise NotImplementedError()
