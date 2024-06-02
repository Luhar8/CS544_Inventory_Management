# echo_server.py
from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu
import json

inventory_items = [
    {"id": 101, "name": "Widget", "quantity": 50},
    {"id": 102, "name": "Gadget", "quantity": 75},
    {"id": 103, "name": "Tool", "quantity": 25}
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