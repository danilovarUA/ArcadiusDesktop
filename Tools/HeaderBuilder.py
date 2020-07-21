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
