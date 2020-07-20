from PermData import PermStorage
from Logger import Logger
from GUI.MainWidget import MainWidget
from Scheduler.AccountThread import AccountThread
from Scheduler.Manager import Manager
from Account.Account import Account

from PyQt5.QtWidgets import QApplication
import sys


def go():
    # Permanent storage set up
    perm_dict = PermStorage().get_dictionary()

    # Logger set up
    logger = Logger(perm_dict)

    # Manager set up
    manager = Manager(logger, perm_dict)

    # GUI and some other weird shit set up
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window = MainWidget(screen.size().width(), screen.size().height(), manager, perm_dict)
    window.show()
    exec_code = app.exec_()
    sys.exit(exec_code)


def fuckAround():
    # Permanent storage set up
    #perm_dict = PermStorage().get_dictionary()

    # Logger set up
    #logger = Logger(perm_dict)

    # Manager set up
    acc = Account("shit11@shit.com", "shit@shit.com", "174")
    success, data = acc.requester.enter()
    print(success)
    print(data)

# go()
fuckAround()
