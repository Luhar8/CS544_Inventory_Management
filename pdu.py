# import json

# class QueryInventoryMessage:
#     def __init__(self, messageType, clientID, timestamp):
#         self.messageType = messageType
#         self.clientID = clientID
#         self.timestamp = timestamp

#     def to_json(self):
#         return json.dumps(self.__dict__)

#     @staticmethod
#     def from_json(json_str):
#         data = json.loads(json_str)
#         return QueryInventoryMessage(**data)

#     def to_bytes(self):
#         return self.to_json().encode('utf-8')

#     @staticmethod
#     def from_bytes(json_bytes):
#         return QueryInventoryMessage.from_json(json_bytes.decode('utf-8'))


# class InventoryResponseMessage:
#     def __init__(self, messageType, itemID, itemName, quantity):
#         self.messageType = messageType
#         self.itemID = itemID
#         self.itemName = itemName
#         self.quantity = quantity

#     def to_json(self):
#         return json.dumps(self.__dict__)

#     @staticmethod
#     def from_json(json_str):
#         data = json.loads(json_str)
#         return InventoryResponseMessage(**data)

#     def to_bytes(self):
#         return self.to_json().encode('utf-8')

#     @staticmethod
#     def from_bytes(json_bytes):
#         return InventoryResponseMessage.from_json(json_bytes.decode('utf-8'))

# pdu.py

import json
import struct

class QueryInventoryMessage:
    def __init__(self, version, clientID, timestamp):
        self.version = version
        self.clientID = clientID
        self.timestamp = timestamp
        self.type = 'query'

    def to_bytes(self):
        # Simple JSON-based serialization
        return json.dumps({
            'type': self.type,
            'version': self.version,
            'clientID': self.clientID,
            'timestamp': self.timestamp
        }).encode('utf-8')

    @classmethod
    def from_bytes(cls, data):
        # Deserialize from JSON
        obj = json.loads(data.decode('utf-8'))
        return cls(obj['version'], obj['clientID'], obj['timestamp'])

class InventoryResponseMessage:
    def __init__(self, version, itemID, itemName, quantity):
        self.version = version
        self.itemID = itemID
        self.itemName = itemName
        self.quantity = quantity

    def to_bytes(self):
        # Simple JSON-based serialization
        return json.dumps({
            'version': self.version,
            'itemID': self.itemID,
            'itemName': self.itemName,
            'quantity': self.quantity
        }).encode('utf-8')

    @classmethod
    def from_bytes(cls, data):
        # Deserialize from JSON
        obj = json.loads(data.decode('utf-8'))
        return cls(obj['version'], obj['itemID'], obj['itemName'], obj['quantity'])

class UpdateInventoryMessage:
    def __init__(self, version, itemID, newQuantity):
        self.version = version
        self.itemID = itemID
        self.newQuantity = newQuantity
        self.type = 'update'

    def to_bytes(self):
        # Simple JSON-based serialization
        return json.dumps({
            'type' : self.type,
            'version': self.version,
            'itemID': self.itemID,
            'newQuantity': self.newQuantity
        }).encode('utf-8')

    @classmethod
    def from_bytes(cls, data):
        # Deserialize from JSON
        obj = json.loads(data.decode('utf-8'))
        return cls(obj['version'], obj['itemID'], obj['newQuantity'])
    
class DeleteInventoryMessage:
    def __init__(self, version, itemID):
        self.version = version
        self.itemID = itemID
        self.type = 'delete'

    def to_bytes(self):
        # Simple JSON-based serialization
        return json.dumps({
            'type': self.type,
            'version': self.version,
            'itemID': self.itemID
        }).encode('utf-8')

    @classmethod
    def from_bytes(cls, data):
        # Deserialize from JSON
        obj = json.loads(data.decode('utf-8'))
        return cls(obj['version'], obj['itemID'])
    
class AddInventoryMessage:
    def __init__(self, version, itemId, itemName, quantity):
        self.version = version
        self.itemId = itemId
        self.itemName = itemName
        self.quantity = quantity
        self.type = 'add'

    def to_bytes(self):
        return json.dumps({
            'type': self.type,
            'version': self.version,
            'itemId': self.itemId,
            'itemName': self.itemName,
            'quantity': self.quantity
        }).encode('utf-8')

    @classmethod
    def from_bytes(cls, data):
        obj = json.loads(data.decode('utf-8'))
        return cls(obj['version'],obj['itemId'], obj['itemName'], obj['quantity'])
