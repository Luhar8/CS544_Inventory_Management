from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu

async def inventory_server_proto(scope, conn: EchoQuicConnection):
    message = await conn.receive()
    qim = pdu.QueryInventoryMessage.from_bytes(message.data)
    print("[svr] Query received for client ID:", qim.clientID)

    # Assume inventory data is retrieved here
    item_id = 101
    item_name = "Widget"
    quantity = 50
    irm = pdu.InventoryResponseMessage(2, item_id, item_name, quantity)
    
    rsp_msg = irm.to_bytes()
    rsp_event = QuicStreamEvent(message.stream_id, rsp_msg, False)
    await conn.send(rsp_event)
