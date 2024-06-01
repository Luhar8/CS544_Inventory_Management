# echo_server.py
from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu

inventory_items = [
    {"id": 101, "name": "Widget", "quantity": 50},
    {"id": 102, "name": "Gadget", "quantity": 75},
    {"id": 103, "name": "Tool", "quantity": 25}
]

async def inventory_server_proto(scope, conn: EchoQuicConnection):
    message = await conn.receive()
    qim = pdu.QueryInventoryMessage.from_bytes(message.data)
    print("[svr] Query received for client ID:", qim.clientID)

    for item in inventory_items:
        irm = pdu.InventoryResponseMessage(2, item['id'], item['name'], item['quantity'])
        rsp_msg = irm.to_bytes()
        rsp_event = QuicStreamEvent(message.stream_id, rsp_msg, False)
        await conn.send(rsp_event)
    # Optionally, close the stream after sending all items
    await conn.send(QuicStreamEvent(message.stream_id, b'', True))
