# echo_server.py
from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu
import json

inventory_items = [
    {"id": 101, "name": "Apples", "quantity": 50},
    {"id": 102, "name": "Whole Milk", "quantity": 75},
    {"id": 103, "name": "Coffee", "quantity": 25},
    {"id": 104, "name": "Yogurt", "quantity": 30}
]

async def inventory_server_proto(scope, conn: EchoQuicConnection):
    while True:
        message = await conn.receive()
        print("[svr] Received message")
        
        data = json.loads(message.data.decode('utf-8'))
        if data['type'] == 'query':
            print("[svr] Query received")
            for item in inventory_items:
                irm = pdu.InventoryResponseMessage(2, item['id'], item['name'], item['quantity'])
                rsp_event = QuicStreamEvent(message.stream_id, irm.to_bytes(), False)
                await conn.send(rsp_event)
            await conn.send(QuicStreamEvent(message.stream_id, b'', True))  # Close this stream

        elif data['type'] == 'update':
            print("[svr] Update received")
            item_to_update = next((item for item in inventory_items if item['id'] == data['itemID']), None)
            if item_to_update:
                item_to_update['quantity'] = data['newQuantity']
                print(f"[svr] Updated item {data['itemID']} to new quantity {data['newQuantity']}")
            
            # Send updated inventory list
            for item in inventory_items:
                irm = pdu.InventoryResponseMessage(2, item['id'], item['name'], item['quantity'])
                await conn.send(QuicStreamEvent(message.stream_id, irm.to_bytes(), False))
            await conn.send(QuicStreamEvent(message.stream_id, b'', True))

        elif data['type'] == 'delete':
            print("[svr] Delete received")
            item_to_delete = next((item for item in inventory_items if item['id'] == data['itemID']), None)
            if item_to_delete:
                inventory_items.remove(item_to_delete)
                print(f"[svr] Deleted item {data['itemID']}")

            # Send updated inventory list
            for item in inventory_items:
                irm = pdu.InventoryResponseMessage(2, item['id'], item['name'], item['quantity'])
                await conn.send(QuicStreamEvent(message.stream_id, irm.to_bytes(), False))
            await conn.send(QuicStreamEvent(message.stream_id, b'', True))

        elif data['type'] == 'add':
            print("[svr] Add received")
            new_item_id = data['itemId']
            new_item_name = data['itemName']
            new_item_quantity = data['quantity']
            inventory_items.append({"id": new_item_id, "name": new_item_name, "quantity": new_item_quantity})
            print(f"[svr] Added new item {new_item_name} with ID {new_item_id} and quantity {new_item_quantity}")
            
            # Send updated inventory list
            for item in inventory_items:
                irm = pdu.InventoryResponseMessage(2, item['id'], item['name'], item['quantity'])
                await conn.send(QuicStreamEvent(message.stream_id, irm.to_bytes(), False))
            await conn.send(QuicStreamEvent(message.stream_id, b'', True))