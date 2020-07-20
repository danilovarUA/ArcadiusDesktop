class Server:
    def __init__(self, server_id):
        self.server_id = server_id
        self.last_login = None
        self.status_description = None
        self.name = None
        self.region_url = None
        self.map_url = None
        self.url = None

    def update_with_data(self, data):
        try:
            for world in data["loginConnectedWorlds"]:
                if world["id"].decode('ascii') == self.server_id:
                    self.last_login = world["lastLoginDate"]
                    self.status_description = world["worldStatus"]["description"].decode("ascii")
                    break
        except KeyError:
            pass
        for world in data["allAvailableWorlds"]:
            if world["id"].decode('ascii') == self.server_id:  # TODO: remove ascii decoding once all data is decoded
                self.name = world["name"]
                try:
                    self.region_url = world["regionDataURL"]
                except KeyError:
                    pass
                self.map_url = world["mapURL"]
                self.url = world["url"].decode('ascii')
                break
