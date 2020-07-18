from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
import Constants
from Data import get_logs
from GUI import Translation
from Tool import text_to_widget


class OverviewPage(QWidget):
    def __init__(self, accounts_thread):
        super().__init__()

        self.accounts_thread = accounts_thread

        layout = QGridLayout()
        # TODO Add tables here
        # layout.addWidget(self.table_widget())
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.setInterval(Constants.INTERFACE_UPDATE_TIMEOUT)
        self.timer.timeout.connect(self.update_all)
        self.timer.start()
        self.update_all()

    def update_all(self):
        pass

    def table_accounts(self):
        pass
        # TODO No table here yet

    def table_habitats(self):
        pass
        # TODO No table here yet

    def table_development(self):
        pass
        # TODO No table here yet
