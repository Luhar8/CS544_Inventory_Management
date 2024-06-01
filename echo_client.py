from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu
import time

async def inventory_client_proto(scope, conn: EchoQuicConnection):
    # Create QIM and send
    qim = pdu.QueryInventoryMessage(1, 12345, int(time.time()))
    new_stream_id = conn.new_stream()
    qs = QuicStreamEvent(new_stream_id, qim.to_bytes(), False)
    await conn.send(qs)

    # Receive IRM
    message = await conn.receive()
    irm = pdu.InventoryResponseMessage.from_bytes(message.data)
    print('[cli] Inventory info received:', irm.itemName, irm.quantity)
