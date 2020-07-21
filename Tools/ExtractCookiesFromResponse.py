def extract_cookies(response):
    cookie_data_list = response.cookies.items()
    cookie_data_dict = {}
    for element in cookie_data_list:
        cookie_data_dict[element[0]] = element[1]
    return cookie_data_dict