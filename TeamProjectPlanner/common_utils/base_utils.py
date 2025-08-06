import os
import json


def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as json_file:
            return json.load(json_file)
    return []


def save_json(path, data):
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=2)
