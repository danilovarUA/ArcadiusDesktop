from datetime import datetime


class Logger:
    def __init__(self, permDict):
        self.permDict = permDict

    def add_log(self, text, source, account, user_visible=False, finished=None):
        name = account.data["player"][account.player_id]["nick"]
        new_log = {"text": text, "source": source, "user_visible": user_visible, "finished": finished, "error": None,
                   "time": datetime.now(), "email": account.email, "server": account.server["name"], "name": name}
        print(new_log)
        self.permDict["logs"]["{}-{}-{}".format(new_log["email"], new_log["server"], new_log["time"])] = new_log
        return new_log

    def finish_log(self, log, success, error):
        self.permDict["logs"]["{}-{}-{}".format(log["email"], log["server"], log["time"])]["finished"] = success
        self.permDict["logs"]["{}-{}-{}".format(log["email"], log["server"], log["time"])]["error"] = error

