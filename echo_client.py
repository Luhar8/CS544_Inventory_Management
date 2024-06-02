# echo_client.py
from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu
import time
import json

async def inventory_client_proto(scope, conn: EchoQuicConnection):
    # Create QIM and send
    qim = pdu.QueryInventoryMessage(1, 12345, int(time.time()))
    new_stream_id = conn.new_stream()
    qs = QuicStreamEvent(new_stream_id, qim.to_bytes(), False)
    await conn.send(qs)

    # Receive multiple IRMs
    while True:
        message = await conn.receive()
        if message.end_stream:
            break
        irm = pdu.InventoryResponseMessage.from_bytes(message.data)
        print('[cli] Inventory info received:', irm.itemName, irm.quantity)

# echo_client.py
# async def inventory_client_proto(scope, conn: EchoQuicConnection):
#     new_stream_id = conn.new_stream()
    
#     # Example command to update an item's quantity
#     update_request = json.dumps({'action': 'update', 'item_id': 101, 'quantity': -10}).encode('utf-8')
#     await conn.send(QuicStreamEvent(new_stream_id, update_request, False))
    
#     # Request to list all inventory items
#     list_request = json.dumps({'action': 'list'}).encode('utf-8')
#     await conn.send(QuicStreamEvent(new_stream_id, list_request, False))
    
#     # Receive and process responses
#     while True:
#         message = await conn.receive()
#         if message.end_stream:
#             break
#         response = json.loads(message.data.decode('utf-8'))
#         print('Server response:', response)

