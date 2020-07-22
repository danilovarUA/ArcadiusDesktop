def un_byte_data(data):
    if type(data) is bytes:
        data = data.decode("ascii")
    elif type(data) is dict:
        for key in data:
            data[key] = un_byte_data(data[key])
    elif type(data) is list:
        for key in range(len(data)):
            data[key] = un_byte_data(data[key])
    return data
