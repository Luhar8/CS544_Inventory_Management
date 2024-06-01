# echo_server.py
from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu
import json

inventory_items = {
    101: {"name": "Widget", "quantity": 50},
    102: {"name": "Gadget", "quantity": 75},
    103: {"name": "Tool", "quantity": 25}
}

# async def inventory_server_proto(scope, conn: EchoQuicConnection):
#     message = await conn.receive()
#     qim = pdu.QueryInventoryMessage.from_bytes(message.data)
#     print("[svr] Query received for client ID:", qim.clientID)

#     for item in inventory_items:
#         irm = pdu.InventoryResponseMessage(2, item['id'], item['name'], item['quantity'])
#         rsp_msg = irm.to_bytes()
#         rsp_event = QuicStreamEvent(message.stream_id, rsp_msg, False)
#         await conn.send(rsp_event)
#     # Optionally, close the stream after sending all items
#     await conn.send(QuicStreamEvent(message.stream_id, b'', True))

# echo_server.py
async def inventory_server_proto(scope, conn: EchoQuicConnection):
    while True:
        message = await conn.receive()
        if message.end_stream:
            break
        request = json.loads(message.data.decode('utf-8'))
        action = request.get('action')
        
        if action == 'update':
            # Example: {'action': 'update', 'item_id': 101, 'quantity': 5}
            item_id = request['item_id']
            quantity_change = request['quantity']
            print("Item_id", item_id, "Quantity", quantity_change)
            if item_id in inventory_items:
                inventory_items[item_id]['quantity'] += quantity_change
                response = {'status': 'success', 'description': 'Quantity updated'}
            else:
                response = {'status': 'failed', 'description': 'Item not found'}
        elif action == 'list':
            # Return a list of all inventory items
            response = {'status': 'success', 'inventory': list(inventory_items.values())}
        else:
            response = {'status': 'error', 'description': 'Invalid action'}
        
        rsp_msg = json.dumps(response).encode('utf-8')
        rsp_event = QuicStreamEvent(message.stream_id, rsp_msg, False)
        await conn.send(rsp_event)

