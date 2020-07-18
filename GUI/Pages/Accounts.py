from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGridLayout, QWidget, QTabWidget, QTableWidgetItem, QLineEdit, QMessageBox
import Constants
from GUI import Translation
from Tool import text_to_widget
from Requester import Requests
from Requester.Requester import send_lak_request_template
import hashlib
from Database.Models import Account as Database_Account
from Data import add_account
from GUI.Template.Table import Table
from GUI.Template.Label import Label
from GUI.Template.Button import Button


class AccountsTabsWidget(QWidget):
  def __init__(self, accounts_thread):
    super().__init__()
    self.accounts_thread = accounts_thread
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

    self.tab_widget.addTab(Overview(self.accounts_thread), Translation.get_text("overview"))
    self.tab_widget.addTab(AddAccount(self.accounts_thread), Translation.get_text("add_accounts"))


class Overview(QWidget):
    def __init__(self, accounts_thread):
        super().__init__()
        self.accounts_thread = accounts_thread
        self.setLayout(self.general_layout())
        self.timer = QTimer()
        self.timer.setInterval(Constants.INTERFACE_UPDATE_TIMEOUT)
        self.timer.timeout.connect(self.update_accounts)
        self.timer.start()
        self.update_accounts()

    def general_layout(self):
        general_layout = QGridLayout()
        self.table_widget()
        general_layout.addWidget(self.accounts_table, 0, 0)
        general_layout.addLayout(self.buttons_layout(), 1, 0)
        return general_layout

    def table_widget(self):
        self.accounts_table = Table([("", 0),
                                     (Translation.get_text('email'), 150),
                                     (Translation.get_text('server'), 100),
                                     (Translation.get_text('name'), 180),
                                     (Translation.get_text('points'), 150)],
                                    scrolling_off=True,
                                    sorting_off=True)

    def buttons_layout(self):
        layout = QGridLayout()
        remove_account_button = Button(Translation.get_text("remove_accounts"))
        change_password_button = Button(Translation.get_text("change_password"))
        remove_account_button.clicked.connect(self.button_clicked_remove_accounts)
        change_password_button.clicked.connect(self.button_clicked_change_password)
        layout.addWidget(remove_account_button, 0, 0)
        layout.addWidget(change_password_button, 0, 1)
        return layout

    def button_clicked_remove_accounts(self):
        print("remove")
        # TODO 🙄

    def button_clicked_change_password(self):
        print("change ")
        # TODO 🙄

    def update_accounts(self):
        _accounts = {a.order: (a, thread) for a, thread in self.accounts_thread.get_accounts().items()}
        _mapping = {order_orig: order_new for order_new, order_orig in zip(range(len(_accounts)), _accounts.keys())}
        self.accounts = {_mapping[order]: t for order, t in _accounts.items()}
        self.accounts_table.setRowCount(len(self.accounts))

        for index, (database_account, account_thread) in self.accounts.items():
            self.accounts_table.setRowHeight(index, Constants.TABLE_ROW_HEIGHT)
            account = account_thread.account

            player_object = account.data.player_object
            base = account.data.Base

            select = QTableWidgetItem()
            select.setFlags(
                QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            select.setCheckState(QtCore.Qt.Unchecked)
            select.account_thread = account_thread

            self.accounts_table.setItem(index, 0, select)
            self.accounts_table.setItem(index, 1, text_to_widget(account.email, center=True))
            self.accounts_table.setItem(index, 2, text_to_widget(account.world_info['name'], center=True))

            if account_thread.is_data_ready:
                self.accounts_table.setItem(index, 3, text_to_widget(player_object.get('nick', ''), center=True))
                self.accounts_table.setItem(index, 4,
                                                   text_to_widget(str(player_object.get('points', '')), center=True))
            else:
                for i in range(3, 5):
                    self.accounts_table.setItem(index, i, text_to_widget(''))


def show_popup(title, text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.exec_()


class AddAccount(QWidget):
    def __init__(self, accounts_thread):
        super().__init__()
        self.accounts_thread = accounts_thread
        self.setLayout(self.general_layout())

    def general_layout(self):
        general_layout = QGridLayout()
        general_layout.addLayout(self.email_password_layout(), 0, 0)
        self.server_table_widget()
        general_layout.addWidget(self.servers_table, 1, 0)
        add_button = self.add_button_widget()
        general_layout.addWidget(add_button, 2, 0)
        return general_layout

    def add_button_widget(self):
        button = Button(Translation.get_text("add_accounts"))
        button.clicked.connect(self.add_button_clicked)
        return button

    def email_password_layout(self):
        layout = QGridLayout()
        email_label = Label(Translation.get_text("email"))
        password_label = Label(Translation.get_text("password"))
        self.email_field = QLineEdit("")
        self.password_field = QLineEdit("")
        load_servers_button = Button(Translation.get_text("load_servers"))
        load_servers_button.clicked.connect(self.load_servers_clicked)
        layout.addWidget(email_label, 0, 0)
        layout.addWidget(self.email_field, 0, 1)
        layout.addWidget(password_label, 0, 2)
        layout.addWidget(self.password_field, 0, 3)
        layout.addWidget(load_servers_button, 1, 0)
        return layout

    def server_table_widget(self):
        self.servers_table = Table([("", 0),
                                    (Translation.get_text('server'), 100),
                                    (Translation.get_text('id'), 180)],
                                      sorting_off=True)

    def add_button_clicked(self):
        servers_to_connect = []
        for index in range(self.servers_table.rowCount()):
            if self.servers_table.item(index, 0).checkState() == QtCore.Qt.Checked:
                print(self.servers_table.item(index, 1).text())
                servers_to_connect.append(self.servers_table.item(index, 2).text())
        if len(servers_to_connect) == 0:
            show_popup(Translation.get_text("error"),
                            Translation.get_text("no_servers_selected_popup"))
        for server_id in servers_to_connect:
            account_database = Database_Account()
            account_database.email = self.email_field.text()
            account_database.password = hashlib.sha256(self.password_field.text().encode("utf-8")).hexdigest()
            account_database.world = int(server_id)
            account_database.active = True
            account_database.order = len(self.accounts_thread.get_accounts())
            result = self.accounts_thread.add_account(account_database)
            if result:
                add_account(account_database.email, account_database.password, account_database.world)
        self.fill_table_widget(None)  # clean servers table

    def fill_table_widget(self, response):
        try:
            connected_worlds_ids = [world["id"] for world in response["login_connected_worlds"]]
            worlds = [world for world in response["all_available_worlds"] if world["id"] in connected_worlds_ids]
        except:
            worlds = []
        self.servers_table.setRowCount(len(worlds))

        for index in range(len(worlds)):
            select = QTableWidgetItem()
            select.setFlags(
                QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            select.setCheckState(QtCore.Qt.Unchecked)
            # select.server_name = account_thread
            self.servers_table.setItem(index, 0, select)
            self.servers_table.setItem(index, 1, text_to_widget(worlds[index]["name"], center=True))
            self.servers_table.setItem(index, 2, text_to_widget(worlds[index]["id"], center=True))

    def load_servers_clicked(self):
        password = hashlib.sha256(self.password_field.text().encode("utf-8")).hexdigest()
        request_template = Requests.worlds(self.email_field.text(), password, Constants.DEVICE_ID,
                                           Constants.DEVICE_GROUP, Constants.IOS_VERSION)
        res = send_lak_request_template(request_template, None)
        if "info" in res:
            show_popup(Translation.get_text("tab_accounts_popup_error"),
                            Translation.get_text("tab_accounts_wrong_credentials_popup_text"))
            self.fill_table_widget(None)
        else:
            self.fill_table_widget(res)
