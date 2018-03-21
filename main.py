import sys
from task1 import Task1
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("КГГ")
        self.setGeometry(200, 120, 1000, 700)
        self.tasks = [Task1(self)]
        self.task = self.tasks[0]
        self.setCentralWidget(self.task)
        self.init_ui()

    def init_ui(self):
        menu_bar = self.menuBar()
        task_menu = menu_bar.addMenu('&Задача')

        task1 = QAction('Задача 1', self)
        task1.setShortcut('Ctrl+1')
        task1.triggered.connect(self.set_task(0))

        task_menu.addAction(task1)

        self.show()

    def set_task(self, index):
        def set_task_of_index():
            self.task = self.tasks[index]
            self.setCentralWidget(self.task)

        return set_task_of_index


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


"""
    TODO: обработать деление на 0, константы 
"""