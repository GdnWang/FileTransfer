import json
import os


class set:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

        if os.path.exists(filename):
            with open(filename, "r") as settings:
                self.data = json.load(settings)
        else:
            self.data = {
                "UploadServer":{
                    "save_path" : "",
                    "port"      : 9091,
                },
                "DownloadServer":{
                    "port"      : 9092
                }
            }
            self.save()

    def save(self):
        with open(self.filename, "w") as settings:
            json.dump(self.data, settings, indent=4)

    def get(self, key_path, default=None):
        keys = key_path.split(".")
        value = self.data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key_path, value):
        keys = key_path.split(".")
        current = self.data
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
        self.save()

if __name__ == "__main__":
    settings = set("config.json")
    print(type(settings.get("UploadServer.port")))