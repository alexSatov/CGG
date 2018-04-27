from math import inf

from task import Task


def f(x: float) -> float:
    try:
        return 1 / x
    except ZeroDivisionError:
        return inf


class Task3(Task):
    def __init__(self, main_window):
        super().__init__(main_window)

    def init_ui(self) -> None:
        pass
