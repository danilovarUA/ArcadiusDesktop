from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidgetItem
import Constants
from GUI.Translation import Translation
from GUI.Template.Table import Table
from GUI.Template.TextWidget import TextWidget


def checkbox_handler(item: QTableWidgetItem):
    try:
        account_thread = item.account_thread
    except:
        return
    if item.checkState() == 0:
        account_thread.deactivate()
    if item.checkState() == 2:
        account_thread.activate()


class OverviewPage(QWidget):
    def __init__(self, manager, perm_dict):
        super().__init__()
        self.perm_dict = perm_dict
        self.manager = manager
        self.translation = Translation(perm_dict)

        # self.accounts_table_widget = Table([("", 0),
        #                                     (self.translation.get_text('server'), 200),
        #                                     (self.translation.get_text('license'), 200),
        #                                     (self.translation.get_text('mail'), 200),
        #                                     (self.translation.get_text('name'), 200),
        #                                     (self.translation.get_text('points'), None),
        #                                     (self.translation.get_text('attacks'), 80),
        #                                     (self.translation.get_text('messages'), 80),
        #                                     (self.translation.get_text('reports'), 80),
        #                                     ("", 0),
        #                                     (self.translation.get_text('error'), 243), ],
        #                                    scrolling_off=True,
        #                                    table_click_handler=self.update_accounts,
        #                                    item_click_handler=checkbox_handler)
        # TODO Bug here. Supposedly due to that kind of sorting not changing .order of accounts after sorting accounts
        #  table start displaying something fucked up

        self.log_table_widget = Table([(self.translation.get_text('time'), 150),
                                       (self.translation.get_text('server'), 150),
                                       (self.translation.get_text('mail'), 180),
                                       (self.translation.get_text('name'), 150),
                                       (self.translation.get_text('module'), 150),
                                       (self.translation.get_text('text'), 800)],
                                      scrolling_off=True,
                                      sorting_off=True)

        layout = QGridLayout()
        #layout.addWidget(self.accounts_table_widget, 0, 0)
        layout.addWidget(self.log_table_widget, 1, 0)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.setInterval(Constants.INTERFACE_UPDATE_TIMEOUT)
        self.timer.timeout.connect(self.update_all)
        self.timer.start()
        self.update_all()

    def update_all(self):
        self.update_logs()
        # self.update_accounts()

    def update_logs(self):
        logs = list(reversed(self.perm_dict["logs"]))[:Constants.LOGS_MAX_DISPLAY_AMOUNT]
        self.log_table_widget.setRowCount(len(logs))
        for log_counter in range(len(logs)):
            log = logs[log_counter]
            self.log_table_widget.setRowHeight(log_counter, Constants.TABLE_ROW_HEIGHT)
            self.log_table_widget.setItem(log_counter, 0,
                                          TextWidget(log["time"].strftime('%T %d.%m.%Y')))
            self.log_table_widget.setItem(log_counter, 1, TextWidget(log["server"])) # TODO remake
            self.log_table_widget.setItem(log_counter, 2, TextWidget(str(log["email"])))  # TODO supposed to be a class Account here
            self.log_table_widget.setItem(log_counter, 3, TextWidget(log["name"]))
            self.log_table_widget.setItem(log_counter, 4, TextWidget(log["source"]))
            self.log_table_widget.setItem(log_counter, 5, TextWidget(log["text"]))

    def update_accounts(self):
        _accounts = {a.order: (a, thread) for a, thread in self.accounts_thread.get_accounts().items()}
        _mapping = {order_orig: order_new for order_new, order_orig in zip(range(len(_accounts)), _accounts.keys())}
        self.accounts = {_mapping[order]: t for order, t in _accounts.items()}

        self.accounts_table_widget.setRowCount(len(self.accounts))

        for index, (database_account, account_thread) in self.accounts.items():
            self.accounts_table_widget.setRowHeight(index, Constants.TABLE_ROW_HEIGHT)
            account = account_thread.account

            player_object = account.data.player_object
            base = account.data.Base

            active = QTableWidgetItem()
            active.setFlags(
                QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled |
                QtCore.Qt.ItemIsUserCheckable)
            active.setCheckState(QtCore.Qt.Checked if database_account.active else QtCore.Qt.Unchecked)
            active.account_thread = account_thread

            status = QTableWidgetItem()
            status.setFlags(QtCore.Qt.ItemIsEnabled)
            status.setBackground(account_thread.status_color)

            self.accounts_table_widget.setItem(index, 0, active)
            self.accounts_table_widget.setItem(index, 1, TextWidget(account.world_info['name'], center=True))
            self.accounts_table_widget.setItem(index, 2, TextWidget("(some date)", center=True))
            self.accounts_table_widget.setItem(index, 3, TextWidget(account.email, center=True))
            self.accounts_table_widget.setItem(index, 9, status)
            self.accounts_table_widget.setItem(index, 10, TextWidget(account_thread.status_text, center=True))

            if account_thread.is_data_ready:
                self.accounts_table_widget.setItem(index, 4, TextWidget(player_object.get('nick', ''), center=True))
                self.accounts_table_widget.setItem(index, 5,
                                                   TextWidget(str(player_object.get('points', '')), center=True))
                self.accounts_table_widget.setItem(index, 6, TextWidget(str(len(base.habitat_under_attack_array)),
                                                                            center=True))
                self.accounts_table_widget.setItem(index, 7,
                                                   TextWidget(str(base.unread_discussion_count), center=True))
                self.accounts_table_widget.setItem(index, 8, TextWidget(str(base.unread_report_count), center=True))
            else:
                for i in range(4, 9):
                    self.accounts_table_widget.setItem(index, i, TextWidget(''))
