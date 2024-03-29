# -*- coding: utf-8 -*-
# Ben Humphrey
# github.com/cxmplex

import json


def get_config(block, key):
    with open("config.json") as config:
        data = json.load(config)
    config.close()
    return data[block][key]
