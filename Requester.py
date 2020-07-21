from Constants import WORLDS_URL, REQUEST_TIMEOUT
import requests
import hashlib
from bplist.bplist import BPListReader


class Requester:
    def __init__(self, account):
        self.email = account.email
        self.password_hashed = hashlib.sha256(account.password.encode("utf-8")).hexdigest()
        self.header = create_header()
        self.cookies = None
        self.map_url = None
        self.regional_data_url = None
        self.account = account

    def make(self, url, params, save_cookies=False):
        if "lordsandknights.com" not in url:
            url = self.account.server["url"]["main"] + "/wa/" + url
        try:
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
                self.account.data.parse_dict(to_use)
                return [True, to_use]
        except Exception as error:
            return [False, str(error)]

    def enter(self):
        worlds_result = self.worlds()
        if not worlds_result[0]:
            return worlds_result

        token_result = self.token()
        if not token_result[0]:
            self.header = create_header()
            return token_result

        login_result = self.login()
        if not login_result[0]:
            self.header = create_header()
        return login_result

    def token(self):
        url = "LoginAction/token"
        params = {
            "login": self.email,
            "password": self.password_hashed,
            "deviceType": "Email",
        }
        result = self.make(url=url,
                           params=params,
                           save_cookies=True)
        self.account.player_id = self.cookies["playerID"]
        return result

    def login(self):
        url = "LoginAction/login"
        params = {}
        return self.make(url, params)

    def worlds(self):
        url = WORLDS_URL
        params = {
            "login": self.email,
            "deviceId": self.email,
            "password": self.password_hashed,
            "deviceType": "Email",
        }
        success, data = self.make(url, params)
        if success:
            self.account.update_server(data)
        return success, data


def extract_cookies(response):
    cookie_data_list = response.cookies.items()
    cookie_data_dict = {}
    for element in cookie_data_list:
        cookie_data_dict[element[0]] = element[1]
    return cookie_data_dict


def create_header(cookie_data_dictionary=None):
    cookie_data_string = ""
    if cookie_data_dictionary is None:
        cookie_data_dictionary = {}
    cookie_data_dictionary.update({"G_ENABLED_IDPS": "google"})
    for element in cookie_data_dictionary:
        cookie_data_string += element + "=" + cookie_data_dictionary[element] + ";"
    login_headers = \
        {
            "XYClient-Capabilities": "base,fortress,city,partialUpdate,simplePlayerReport,requestInformation," +
                                     "starterpack,pushevent,regions",
            "Cookie": cookie_data_string,
            "Accept": "application/x-bplist",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "XYClient-Platform": "ios",
            "User-Agent": "Lords & Knights/8.4.2 (iOS 13.5 / iPhone12,3)",
            "Accept-Language": "en-EN",
        }
    return login_headers
