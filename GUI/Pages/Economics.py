from PyQt5.QtWidgets import *
from GUI import Translation
from GUI.Pages.EconomicsSubpages.Overview import OverviewPage


class MainWidget(QWidget):
  def __init__(self, accounts_thread):
    super().__init__()
    self.accounts_thread = accounts_thread
    self.setMinimumSize(1260, 800)
    layout = QGridLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    self.tab_widget = QTabWidget()
    layout.addWidget(self.tab_widget)
    self.setLayout(layout)
    self.restart()

  def restart(self):
    while self.tab_widget.count() > 0:
      self.tab_widget.removeTab(0)

    self.tab_widget.addTab(OverviewPage(self.accounts_thread), Translation.get_text("overview"))
