import csv
import json

class CsvParser:
    def __init__(self, path, extra_fields):
        self.reader = csv.DictReader(open(path))
        self.extra_fields = extra_fields

    def get_line_json(self):
        try:
            line = next(self.reader)
        except StopIteration:
            return None
        line.update(self.extra_fields)
        return json.dumps(line)
