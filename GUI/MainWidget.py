from PyQt5.QtWidgets import QGridLayout, QTabWidget, QWidget
import Constants
from GUI import Translation
from GUI.Pages.Overview import OverviewPage
from GUI.Pages.Settings import SettingsPage
from GUI.Pages.Accounts import AccountsTabsWidget as AccountsWidget
from GUI.Pages.Economics import MainWidget as EconomicsWidget


class MainWidget(QWidget):
    def __init__(self, accounts_thread, width, height):
        super().__init__()
        self.accounts_thread = accounts_thread

        self.setWindowTitle(Constants.WINDOW_NAME)
        self.resize(width, height)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

        self.show()

        self.restart()

    def restart(self):
        while self.tab_widget.count() > 0:
            self.tab_widget.removeTab(0)

        self.tab_widget.addTab(OverviewPage(self.accounts_thread), Translation.get_text("overview"))
        self.tab_widget.addTab(EconomicsWidget(self.accounts_thread), Translation.get_text("economy"))
        self.tab_widget.addTab(QWidget(), Translation.get_text("defense"))
        self.tab_widget.addTab(QWidget(), Translation.get_text("attack"))
        self.tab_widget.addTab(QWidget(), Translation.get_text("tools"))
        self.tab_widget.addTab(QWidget(), Translation.get_text("forum"))
        self.tab_widget.addTab(QWidget(), Translation.get_text("messages"))
        self.tab_widget.addTab(QWidget(), Translation.get_text("reports"))
        self.tab_widget.addTab(AccountsWidget(self.accounts_thread), Translation.get_text("accounts"))
        self.tab_widget.addTab(QWidget(), Translation.get_text("logs"))
        self.tab_widget.addTab(SettingsPage(self.accounts_thread, self), Translation.get_text("settings"))
