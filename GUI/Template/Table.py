from PyQt5.QtWidgets import QTableWidget
import Constants
from PyQt5 import QtCore


class Table(QTableWidget):

    def __init__(self,
                 columns,
                 scrolling_off=False,
                 sorting_off=False,
                 table_click_handler=None,
                 item_click_handler=None):
        # Columns is a list of tuples (header, width) if width == 0 MIN_ROW_WIDTH is used instead, if width is None -
        # it will not be specified
        super().__init__()

        if not sorting_off:
            self.setSortingEnabled(True)

        self.verticalHeader().setMinimumSectionSize(Constants.TABLE_MINIMUM_WIDTH)
        self.horizontalHeader().setMinimumSectionSize(Constants.TABLE_MINIMUM_WIDTH)

        self.setRowCount(0)
        self.setColumnCount(len(columns))

        self.move(0, 0)

        if scrolling_off:
            self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        headers = [column[0] for column in columns]
        self.setHorizontalHeaderLabels(headers)

        widths = [column[1] for column in columns]
        for index in range(len(widths)):
            width = widths[index]
            if width is None:
                continue
            if width == 0:
                width = Constants.TABLE_MINIMUM_WIDTH
            self.setColumnWidth(index, width)

        if table_click_handler is not None:
            self.clicked.connect(table_click_handler)

        if item_click_handler is not None:
            self.itemClicked.connect(item_click_handler)
