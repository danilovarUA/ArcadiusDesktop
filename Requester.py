import requests
import hashlib


REQUEST_TIMEOUT = 6
SERVER_URL = "https://backend2.lordsandknights.com/XYRALITY/WebObjects/LKWorldServer-RE-DE-4.woa/wa/"


class Requester:
    def __init__(self, email, password):
        self.email = email
        self.password_hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
        self.header = create_header()
        self.cookies = None

    def make(self, url, params, save_cookies=False):
        if "lordsandknights.com" not in url:
            url = SERVER_URL + url

        try:
            response = requests.get(url, params=params, headers=self.header, timeout=REQUEST_TIMEOUT)
            if save_cookies:
                to_check = response.json
                to_use = extract_cookies(response)
            else:
                to_check = response.json
                to_use = to_check
            if "error" in to_check:
                raise ValueError("Response contains error saying: " + to_check["error"])
            if save_cookies:
                self.header = create_header(to_use)
                self.cookies = to_use
                return [True, "Headers updated"]
            else:
                return [True, to_use]
        except Exception as error:
            return [False, str(error)]

    def enter(self):
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
        return self.make(url=url,
                         params=params,
                         save_cookies=True)

    def login(self):
        url = "LoginAction/login"
        params = {}
        return self.make(url, params)


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
