import csv
import json

class CsvParser:
    def __init__(self, path):
        self.reader = csv.DictReader(open(path))

    def get_line_json(self):
        line = next(self.reader)
        if not line:
            return None
        return json.dumps(line)
