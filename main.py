import sys
from task1 import Task1
from task2 import Task2
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("КГГ")
        self.setGeometry(200, 120, 1000, 700)
        self.tasks = [Task1, Task2]
        self.task = self.tasks[0](self)
        self.setCentralWidget(self.task)
        self.init_ui()

    def init_ui(self):
        menu_bar = self.menuBar()
        task_menu = menu_bar.addMenu('&Задача')

        task1 = QAction('Задача 1', self)
        task1.setShortcut('Ctrl+1')
        task1.triggered.connect(self.set_task(0))

        task2 = QAction('Задача 2', self)
        task2.setShortcut('Ctrl+2')
        task2.triggered.connect(self.set_task(1))

        task_menu.addAction(task1)
        task_menu.addAction(task2)

        self.show()

    def set_task(self, index):
        def set_task_of_index():
            self.task = self.tasks[index]
            self.setCentralWidget(self.task(self))

        return set_task_of_index


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
