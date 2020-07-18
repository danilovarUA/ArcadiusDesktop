class Account:
    def __init__(self, email, password, server_id):
        self.email = email
        self.password = password
        self.server_id = server_id
        self.password_hashed = None  # TODO: hash password
        self.data_dict = {}

    def update_dict(self):
        pass  # TODO: recursively update data_dict with new data

d = {"a": ["a1", "a2"], "b": "bb"}
d.update({"a": ["a3"]})
print(d)