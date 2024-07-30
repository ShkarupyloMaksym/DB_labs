import json


def get_creds():
    data = json.load(open('../db/creds.json'))
    return data


if __name__ == '__main__':
    print(get_creds())
