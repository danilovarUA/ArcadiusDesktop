from Account import Account


class Manager:
    def __init__(self, logger, perm_dict, start_all=True):
        self.accounts = []
        if start_all:
            print(perm_dict["accs"])
            for acc_index in perm_dict["accs"]:
                new_account = Account(perm_dict["accs"][acc_index], logger, perm_dict)
                new_account.start()
                self.accounts.append(new_account)
        print("Not a log: Manager started {} account".format(len(self.accounts)))

    def toggle_account(self, email, server_id):
        for account in self.accounts:
            if account.email == email and account.server["id"] == server_id:
                account.active = not account.active
                break
