from Requester import Requester
from Account.Server import Server


class Account:
    def __init__(self, dictionary):
        self.email = dictionary["email"]
        self.password = dictionary["password"]
        self.server = Server(dictionary["server_id"], name=dictionary["server_name"])
        self.requester = Requester(self.email, self.password, self.server)
