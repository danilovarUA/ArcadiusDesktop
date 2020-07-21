"""A dictionary will be dumped to hard drive asynchronously if it was previously changed and loaded on init."""
from collections import UserDict
import pickle
import threading
import time

from Constants import TEMPDICT_STORE_TICK, TEMPDICT_PICKLE_FILENAME, TEMPDICT_GET_DICTIONARY_REATTEMPT


class PermDict(UserDict):
    changed = False

    def __init__(self):
        dictionary =\
            {
                "logs": [],
                "accs": [],
                "settings":
                    {
                        "language": "en"
                    }
            }
        super().__init__(dictionary)

    def __setitem__(self, key, value):
        super(PermDict, self).__setitem__(key, value)
        self.changed = True


class PermDictThread(threading.Thread):
    dictionary = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.load()

    def run(self):
        while True:
            if self.dictionary.changed:
                self.store()
            time.sleep(TEMPDICT_STORE_TICK)

    def load(self):
        try:
            with open(TEMPDICT_PICKLE_FILENAME, 'rb') as file:
                self.dictionary = pickle.load(file)
        except FileNotFoundError:
            self.dictionary = PermDict()

    def store(self):
        print("PermDictThread: store")
        with open(TEMPDICT_PICKLE_FILENAME, 'wb') as file:
            pickle.dump(self.dictionary, file, protocol=pickle.HIGHEST_PROTOCOL)
        self.dictionary.changed = False


class PermStorage:
    dictionary = None

    def __init__(self):
        self.thread = PermDictThread()
        self.thread.start()

    def get_dictionary(self):
        while self.thread.dictionary is None:
            time.sleep(TEMPDICT_GET_DICTIONARY_REATTEMPT)
        self.dictionary = self.thread.dictionary
        return self.dictionary
