import json

class Parser:
    @staticmethod
    def parse_json(data):
        return json.loads(data)

    @staticmethod
    def to_json(data):
        return json.dumps(data, indent=4)