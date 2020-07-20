from Scheduler.AccountThread import AccountThread
from Account.Account import Account


class Manager:
    def __init__(self, logger, perm_dict, start_all=True):
        self.threads = []
        if "accs" not in perm_dict:
            perm_dict["accs"] = []
        if start_all:
            for acc in perm_dict["accs"]:
                new_account = Account(acc["email"], acc["password"], acc["server_id"])
                new_thread = AccountThread(new_account, logger, perm_dict)
                new_thread.start()
                self.threads.append(new_thread)
