from datetime import datetime


class Log:
    def __init__(self, text, source, user_visible=False, finished=False):
        self.text = text
        self.source = source
        self.user_visible = user_visible
        self.finished = finished
        self.error = None
        self.time = datetime.now()

    def to_dict(self):
        log_dict = {"text": }


class Logger:
    def __init__(self, permDict):
        if "logs" not in permDict:
            permDict["logs"] = []
        self.logs = permDict["logs"]

    def add_log(self):
        pass

    def get_log_by_id(self, log_id):
        pass

    def clean_old_logs(self):
        pass