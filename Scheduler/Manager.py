from Scheduler.AccountThread import AccountThread
from Account.Account import Account


class Manager:
    def __init__(self, logger, perm_dict, start_all=True):
        self.threads = []
        if start_all:
            for acc_dict in perm_dict["accs"]:
                new_account = Account(acc_dict)
                new_thread = AccountThread(new_account, logger, perm_dict)
                new_thread.start()
                self.threads.append(new_thread)
