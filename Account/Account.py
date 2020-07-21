from Requester import Requester


class Account:
    def __init__(self, dictionary):
        self.email = dictionary["email"]
        self.password = dictionary["password"]
        self.requester = Requester(self)
        self.server = {"id": dictionary["server_id"],
                       "status": None,
                       "name": dictionary["server_name"],
                       "last_login": None,
                       "urls": {"region": None, "map": None, "main": None}}

    def update_server(self, data):
        try:
            for world in data["loginConnectedWorlds"]:
                if world["id"].decode('ascii') == self.server["id"]:
                    self.server["last_login"] = world["lastLoginDate"]
                    self.server["status"] = world["worldStatus"]["description"].decode("ascii")
                    break
        except KeyError:
            pass
        for world in data["allAvailableWorlds"]:
            if world["id"].decode('ascii') == self.server["id"]:  # TODO: remove ascii decoding once all data is decoded
                self.server["name"] = world["name"]
                try:
                    self.server["url"]["region"] = world["regionDataURL"]
                except KeyError:
                    pass
                self.server["url"]["map"] = world["mapURL"]
                self.server["url"]["main"] = world["url"].decode('ascii')
                break
