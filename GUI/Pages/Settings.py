from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGridLayout, QWidget, QVBoxLayout, QComboBox, QSlider

import Settings
from GUI import Translation
from GUI.Template.Line import HLine, VLine
from GUI.Template.Label import Label


class SettingsPage(QWidget):
    def __init__(self, accounts_thread, main_widget):
        super().__init__()
        self.accounts_thread = accounts_thread
        self.main_widget = main_widget
        self.init_base_layout()
        self.init_left_layout()
        self.init_center_layout()
        self.init_right_layout()
        self.setLayout(self.base_layout)

    def init_base_layout(self):
        self.base_layout = QGridLayout()

        self.base_layout.setAlignment(QtCore.Qt.AlignTop)

        header_left = Label(Translation.get_text('interface'))
        header_center = Label(Translation.get_text('bot'))
        header_right = Label(Translation.get_text('other'))

        header_left.setFixedWidth(400)
        header_center.setFixedWidth(400)
        header_right.setFixedWidth(400)

        self.left_layout = QVBoxLayout()
        self.center_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.left_layout.setAlignment(QtCore.Qt.AlignTop)
        self.center_layout.setAlignment(QtCore.Qt.AlignTop)
        self.right_layout.setAlignment(QtCore.Qt.AlignTop)

        self.base_layout.addWidget(header_left, 0, 0)
        self.base_layout.addWidget(VLine(), 0, 1)
        self.base_layout.addWidget(header_center, 0, 2)
        self.base_layout.addWidget(VLine(), 0, 3)
        self.base_layout.addWidget(header_right, 0, 4)
        self.base_layout.addWidget(HLine(), 1, 0)
        self.base_layout.addWidget(HLine(), 1, 2)
        self.base_layout.addWidget(HLine(), 1, 4)
        self.base_layout.addLayout(self.left_layout, 2, 0)
        self.base_layout.addWidget(VLine(), 2, 1)
        self.base_layout.addLayout(self.center_layout, 2, 2)
        self.base_layout.addWidget(VLine(), 2, 3)
        self.base_layout.addLayout(self.right_layout, 2, 4)

    def init_left_layout(self):
        self.init_left_layout_language()

    def init_center_layout(self):
        self.init_center_layout_minimum_time_between_requests()

    def init_right_layout(self):
        pass

    def init_left_layout_language(self):
        label = Label("{}: ".format(Translation.get_text("language_multi")))

        inp = QComboBox()
        inp.addItems(Translation.LANGUAGES)
        inp.setCurrentText(Settings.get('language'))

        language_layout = QGridLayout()
        language_layout.addWidget(label, 0, 0)
        language_layout.addWidget(inp, 0, 1)

        warning = Label(Translation.get_text('language_warning'))
        warning.setAlignment(QtCore.Qt.AlignCenter)

        inp.currentTextChanged.connect(self.change_language)

        self.left_layout.addLayout(language_layout)
        self.left_layout.addWidget(warning)

    def init_center_layout_minimum_time_between_requests(self):
        label = Label(Translation.get_text('minimum_time_between_requests'))
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.center_layout.addWidget(label)

        selector = QSlider(QtCore.Qt.Horizontal)
        selector.setMinimum(100)
        selector.setMaximum(6000)
        selector.setSingleStep(100)
        selector.setValue(int(Settings.get('minimum_time_between_requests')))
        selector.setTickPosition(QSlider.TicksBelow)
        selector.setTickInterval(100)

        self.center_layout.addWidget(selector)

        label = Label('- ' + str(selector.value() / 1000.0) + ' ' + Translation.get_text('seconds') + ' -')
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.center_layout.addWidget(label)

        self.minimum_time_between_requests_old = int(Settings.get('minimum_time_between_requests'))

        selector.valueChanged.connect(
            lambda x: label.setText('- ' + str(x / 1000.0) + ' ' + Translation.get_text('seconds') + ' -'))

        def sync():
            v1 = selector.value()
            if v1 != self.minimum_time_between_requests_old:
                self.minimum_time_between_requests_old = v1
                Settings.put('minimum_time_between_requests', str(v1))

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(sync)
        self.timer.start()

    def change_language(self, text):
        Settings.put('language', text)
        self.main_widget.restart()
        self.main_widget.tab_widget.setCurrentIndex(self.main_widget.tab_widget.count() - 1)
