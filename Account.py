from Requester import Requester
RELATIONSHIP_NUM_TO_WORD = {"-1": "red", "1": "blue", "2": "green", "3": "orange"}


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

        self.data = {"player": {},
                     "player_rank": {},
                     "alliance": {},
                     "habitat": {},
                     "habitat_unit": [],
                     "report": {},
                     "transit": [],
                     "diplomacy": {"red": [], "green": [], "blue": [], "orange": []}}

        self.player_id = None

    def update_data(self, dict_to_parse):
        try:
            for world in dict_to_parse["loginConnectedWorlds"]:
                if world["id"].decode('ascii') == self.server["id"]:
                    self.server["last_login"] = world["lastLoginDate"]
                    self.server["status"] = world["worldStatus"]["description"].decode("ascii")
                    break
        except KeyError:
            pass
        for world in dict_to_parse["allAvailableWorlds"]:
            if world["id"].decode('ascii') == self.server["id"]:  # TODO: remove ascii decoding once all data is decoded
                self.server["name"] = world["name"]
                try:
                    self.server["url"]["region"] = world["regionDataURL"]
                except KeyError:
                    pass
                self.server["url"]["map"] = world["mapURL"]
                self.server["url"]["main"] = world["url"].decode('ascii')
                break

        # TODO: think about making a list of fields that will be saved here
        if "Data" not in dict_to_parse:
            return
        dict_to_parse = dict_to_parse["Data"]
        # Player from Rating
        try:
            for item in dict_to_parse["playerRanks"]:
                self.data["player_rank"][item["id"]] = item
        except KeyError:
            pass

        # Player
        try:
            for item in dict_to_parse["Player"]:
                self.data["player"][item["id"]] = item
        except KeyError:
            pass

        # Alliance
        try:
            for item in dict_to_parse["Alliance"]:
                self.data["alliance"][item["id"]] = item
        except KeyError:
            pass

        # Habitat
        try:
            for item in dict_to_parse["Habitat"]:
                self.data["habitat"][item["id"]] = item
        except KeyError:
            pass

        # Diplomacy
        try:
            for diplomacy_item in dict_to_parse["Data"]["Diplomacy"]:
                _, target_alliance_id = diplomacy_item['id'].split('-')
                relationship_kind = RELATIONSHIP_NUM_TO_WORD[diplomacy_item["relationship"]]
                self.data["diplomacy"][relationship_kind].append(target_alliance_id)
        except KeyError:
            pass

        # HabitatUnit
        try:
            if "HabitatUnit" in dict_to_parse["Data"]:
                self.data["habitat_unit"] = []  # TODO do I really need to reset previous info here? breaks whole point of Data class
            for item in dict_to_parse["Data"]["HabitatUnit"]:
                self.data["habitat_unit"].append(item)
        except KeyError:
            pass

        # Transit
        try:
            if "Transit" in dict_to_parse["Data"]:
                self.data["transit"] = []  # TODO do I really need to reset previous info here? breaks whole point of Data class
            for item in dict_to_parse["Data"]["Transit"]:
                self.data["transit"].append(item)
        except KeyError:
            pass

        try:
            for item in dict_to_parse["Data"]["Report"]:
                self.data["report"][item["id"]] = item
        except KeyError:
            pass
