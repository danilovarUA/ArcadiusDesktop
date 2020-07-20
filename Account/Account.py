from Requester import Requester
from Account.Server import Server

class Account:
    def __init__(self, email, password, server_id):
        self.email = email
        self.password = password
        self.server = Server(server_id)
        self.password_hashed = None  # TODO: hash password
        self.requester = Requester(email, password, self.server)
