import json
import time

class ChangeLog:
    def __init__(self):
        self.logs = []

    def log(self, action, item_id, details):
        timestamp = int(time.time())
        log_entry = {
            'timestamp': timestamp,
            'action': action,
            'item_id': item_id,
            'details': details
        }
        self.logs.append(log_entry)

    def to_json(self):
        return json.dumps(self.logs, indent=2)

    def from_json(self, data):
        self.logs = json.loads(data)
