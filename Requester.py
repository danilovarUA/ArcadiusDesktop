from Constants import WORLDS_URL, REQUEST_TIMEOUT
import requests
import hashlib
from bplist.bplist import BPListReader
from Tools.ExtractCookiesFromResponse import extract_cookies
from Tools.HeaderBuilder import create_header


class Requester:
    def __init__(self, account):
        self.password_hashed = hashlib.sha256(account.password.encode("utf-8")).hexdigest()
        self.header = create_header()
        self.cookies = None
        self.account = account

    def make(self, url, params, save_cookies=False):
        if "lordsandknights.com" not in url:
            url = self.account.server["url"]["main"] + "/wa/" + url
        #try:  # TODO move back
        response = requests.get(url, params=params, headers=self.header, timeout=REQUEST_TIMEOUT)
        reader = BPListReader(response.content)
        to_check = reader.parse()
        if save_cookies:
            to_use = extract_cookies(response)
        else:
            to_use = to_check
        if "error" in to_check:
            return [False, to_check["error"]]
        if save_cookies:
            self.header = create_header(to_use)
            self.cookies = to_use
            return [True, to_use]
        else:
            self.account.update_data(to_use)
            return [True, to_use]
        #except Exception as error:
            #return [False, str(error)]

    def enter(self):
        worlds_result = self.worlds()
        if not worlds_result[0]:
            self.header = create_header()
            return worlds_result
        print("Got worlds")

        token_result = self.token()
        if not token_result[0]:
            self.header = create_header()
            return token_result
        print("Got token")
        login_result = self.login()
        if not login_result[0]:
            self.header = create_header()
        return login_result

    def token(self):
        url = "LoginAction/token"
        params = {
            "login": self.account.email,
            "password": self.password_hashed,
            "deviceType": "Email",
        }
        result = self.make(url=url,
                           params=params,
                           save_cookies=True)
        if result[0]:
            self.account.player_id = self.cookies["playerID"]
        return result

    def login(self):
        url = "LoginAction/login"
        params = {}
        return self.make(url, params)

    def worlds(self):
        url = WORLDS_URL
        params = {
            "login": self.account.email,
            "deviceId": self.account.email,
            "password": self.password_hashed,
            "deviceType": "Email",
        }
        success, data = self.make(url, params)
        if success:
            self.account.update_data(data)
        return success, data
