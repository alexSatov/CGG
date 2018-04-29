from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QPixmap
from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QLabel, QPushButton, QLayout


class OptionsBar(QWidget):
    def __init__(self, task_widget):
        super().__init__(task_widget)
        self.task_widget = task_widget
        self.area = None
        self.options = []
        self.v_options = []
        self.buttons = []
        self.layout = QHBoxLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self.layout)

    def with_area(self):
        self.area = AreaOptions()
        self.layout.addLayout(self.area)

        return self

    def with_int_options_v(self, top=1, bottom=10,
                           top_name='α', bottom_name='β', min=-10000):
        v_option = VerticalIntOption(top, bottom, top_name, bottom_name, min)

        self.v_options.append(v_option)
        self.layout.addLayout(v_option)

        return self

    def with_int_option(self, name, default=0, min=-10000, max=10000):
        option = IntOption(name, default, min, max)

        self.options.append(option)
        self.layout.addLayout(option)

        return self

    def with_button(self, name, callback):
        button = QPushButton(name, self)
        button.clicked.connect(callback)

        self.buttons.append(button)
        self.layout.addWidget(button)

        return self

    def with_image(self, path):
        pixmap = QPixmap(path)
        label = QLabel()
        label.setPixmap(pixmap)

        self.layout.addWidget(label)

        return self

    def clear(self):
        for i in range(self.layout.count() - 1, -1, -1):
            item = self.layout.takeAt(i)
            self.layout.removeItem(item)


class AreaOptions(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.left_top = QVBoxLayout()
        self.right_bottom = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.left_top.x = IntOption('leftTopX')
        self.left_top.y = IntOption('leftTopY')
        self.right_bottom.x = IntOption('rightBottomX', 400)
        self.right_bottom.y = IntOption('rightBottomY', 400)

        self.left_top.addLayout(self.left_top.x)
        self.left_top.addLayout(self.left_top.y)
        self.right_bottom.addLayout(self.right_bottom.x)
        self.right_bottom.addLayout(self.right_bottom.y)

        self.addLayout(self.left_top)
        self.addLayout(self.right_bottom)


class VerticalIntOption(QVBoxLayout):
    def __init__(self, top, bottom, top_name, bottom_name, min):
        super().__init__()
        self.top = IntOption(top_name, top, min)
        self.bottom = IntOption(bottom_name, bottom, min)

        self.addLayout(self.top)
        self.addLayout(self.bottom)


class IntOption(QHBoxLayout):
    def __init__(self, name, default=0, min=-10000, max=10000):
        super().__init__()
        self.name = name
        self.validator = QIntValidator(min, max)
        self.input = QLineEdit()
        self.input.setText(str(default))
        self.input.setMaximumWidth(60)
        self.input.setValidator(self.validator)
        self.setContentsMargins(0, 0, 20, 0)

        self.addWidget(QLabel(self.name), alignment=Qt.AlignRight)
        self.addWidget(self.input)
