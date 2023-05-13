import csv
import json

class CsvParser:
    def __init__(self, path, extra_fields, batch_size=100):
        self.reader = csv.reader(open(path))
        self.extra_fields = extra_fields
        self.batch_size = batch_size
        self.keys = next(self.reader)
        self.end = False

    def get_line_json(self):
        if self.end: return None
        line_list = [[] for _ in range(len(self.keys))]
        for i in range(self.batch_size):
            try:
                line = next(self.reader)
            except StopIteration:
                if line_list[0] == []:
                    return None
                self.end = True
                break
            for i in range(len(line)):
                line_list[i].append(line[i])
        csv_dict = dict(zip(self.keys, line_list))
        csv_dict.update(self.extra_fields)
        return json.dumps(csv_dict)
