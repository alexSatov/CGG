import sys
from typing import Callable

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction

from task1 import Task1
from task2 import Task2
from task3 import Task3
from task4 import Task4


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("КГГ")
        self.setGeometry(200, 120, 1240, 820)
        self.tasks = [Task1, Task2, Task3, Task4]
        self.setCentralWidget(self.tasks[3](self))
        self.init_ui()

    def init_ui(self) -> None:
        menu_bar = self.menuBar()
        task_menu = menu_bar.addMenu('&Задача')

        for i in range(len(self.tasks)):
            task = QAction(f'Задача {i + 1}', self)
            task.setShortcut(f'Ctrl+{i + 1}')
            task.triggered.connect(self.set_task(i))
            task_menu.addAction(task)

        self.show()

    def set_task(self, index: int) -> Callable[[], None]:
        def set_task_of_index() -> None:
            self.setCentralWidget(self.tasks[index](self))

        return set_task_of_index


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
