import json

class QueryInventoryMessage:
    def __init__(self, messageType, clientID, timestamp):
        self.messageType = messageType
        self.clientID = clientID
        self.timestamp = timestamp

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return QueryInventoryMessage(**data)

    def to_bytes(self):
        return self.to_json().encode('utf-8')

    @staticmethod
    def from_bytes(json_bytes):
        return QueryInventoryMessage.from_json(json_bytes.decode('utf-8'))


class InventoryResponseMessage:
    def __init__(self, messageType, itemID, itemName, quantity):
        self.messageType = messageType
        self.itemID = itemID
        self.itemName = itemName
        self.quantity = quantity

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return InventoryResponseMessage(**data)

    def to_bytes(self):
        return self.to_json().encode('utf-8')

    @staticmethod
    def from_bytes(json_bytes):
        return InventoryResponseMessage.from_json(json_bytes.decode('utf-8'))
