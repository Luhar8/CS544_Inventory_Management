# pdu.py

import json
import struct

class QueryInventoryMessage: #Message definition for initial table
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

class InventoryResponseMessage: #Message definition for Inventory response sent to client
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

class UpdateInventoryMessage: #Message definition for update request sent to server
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
    
class DeleteInventoryMessage: #Message definition for delete request sent to server
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
    
class AddInventoryMessage: #Message definition for add request sent to server
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
