

import json


def get_config(block, key):
    with open("config.json") as config:
        data = json.load(config)
    config.close()
    return data[block][key]
