"""Not an actual TextWidget but a table with one cell. But it is useful so it is her:)"""
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore


class TextWidget(QTableWidgetItem):
    def __init__(self, text, center=True, red=False):
        super().__init__(text)
        self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        if center:
            self.setTextAlignment(QtCore.Qt.AlignHCenter)
        if red:
            self.setForeground(QBrush(QColor(255, 0, 0)))
