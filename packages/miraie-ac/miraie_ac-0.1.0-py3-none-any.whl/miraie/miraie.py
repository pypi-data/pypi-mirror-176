import json


class MirAie:
    def __init__(self, path):
        self.path = path
        self.data = None
        self._load_data()

    def _load_data(self):
        with open(self.path, "r") as f:
            self.data = json.load(f)

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value
        self._save_data()

    def _save_data(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)
