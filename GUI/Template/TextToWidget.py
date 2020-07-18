def text_to_widget(text: str, center: bool = False):
    widget = QTableWidgetItem(text)
    widget.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    if center:
        widget.setTextAlignment(QtCore.Qt.AlignHCenter)
    return widget

# TODO: not finished