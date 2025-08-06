import os
import json
from filelock import FileLock


def load_json(path):
    lock = FileLock(path + ".lock")
    with lock:
        if os.path.exists(path):
            with open(path, "r") as json_file:
                return json.load(json_file)
        return []


def save_json(path, data):
    lock = FileLock(path + ".lock")
    with lock:
        with open(path, "w") as json_file:
            json.dump(data, json_file, indent=2)
