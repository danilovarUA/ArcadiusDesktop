from PermData import PermStorage
from Logger import Logger
from GUI.MainWidget import MainWidget
from Scheduler.Manager import Manager

from PyQt5.QtWidgets import QApplication
import sys


def go(reset_accs=False, reset_logs=False):
    # Permanent storage set up
    perm_dict = PermStorage().get_dictionary()
    print(perm_dict)
    if reset_accs:
        perm_dict["accs"] = {}
        perm_dict["accs"]["shit11@shit.com-230"] = {"email": "shit11@shit.com",
                                            "password": "shit@shit.com",
                                            "name": "shit",
                                            "server_id": "230",
                                            "server_name": "sName",
                                            "position": "0",
                                            }
    if reset_logs:
        perm_dict["logs"] = []
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


go(reset_accs=False, reset_logs=False)
