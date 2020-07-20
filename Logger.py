from datetime import datetime


class Logger:
    def __init__(self, permDict):
        if "logs" not in permDict:
            permDict["logs"] = []
        self.permDict = permDict

    def add_log(self, text, source, account, user_visible=False, finished=None):
        new_log = {"text": text, "source": source, "user_visible": user_visible, "finished": finished, "error": None,
                   "time": datetime.now(), "account": account}
        self.permDict["logs"].append(new_log)
        self.permDict.changed = True
        print(new_log)  # TODO: temporary

    def finish_log(self, log_id, success, error):
        self.permDict["logs"][log_id]["finished"] = success
        if not success:
            self.permDict["logs"][log_id]["error"] = error
        self.permDict.changed = True
