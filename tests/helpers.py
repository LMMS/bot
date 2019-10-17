import json

from types import SimpleNamespace


def load_json_object(path: str):
    with open(path) as f:
        return json.load(f, object_hook=lambda d: SimpleNamespace(**d))
