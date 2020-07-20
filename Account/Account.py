from Requester import Requester


class Account:
    def __init__(self, email, password, server_id):
        self.email = email
        self.password = password
        self.server_id = server_id
        self.password_hashed = None  # TODO: hash password
        self.data_dict = {}
        self.requester = Requester(email, password)
