# # echo_client.py
# import pdu
# import time
# import json

# # async def inventory_client_proto(scope, conn: EchoQuicConnection):
# #     # Create QIM and send
# #     qim = pdu.QueryInventoryMessage(1, 12345, int(time.time()))
# #     new_stream_id = conn.new_stream()
# #     qs = QuicStreamEvent(new_stream_id, qim.to_bytes(), False)
# #     await conn.send(qs)

# #     # Receive multiple IRMs
# #     while True:
# #         message = await conn.receive()
# #         if message.end_stream:
# #             break
# #         irm = pdu.InventoryResponseMessage.from_bytes(message.data)
# #         print('[cli] Inventory info received:', irm.itemName, irm.quantity)

# # echo_client.py
# # async def inventory_client_proto(scope, conn: EchoQuicConnection):
# #     new_stream_id = conn.new_stream()
    
# #     # Example command to update an item's quantity
# #     update_request = json.dumps({'action': 'update', 'item_id': 101, 'quantity': -10}).encode('utf-8')
# #     await conn.send(QuicStreamEvent(new_stream_id, update_request, False))
    
# #     # Request to list all inventory items
# #     list_request = json.dumps({'action': 'list'}).encode('utf-8')
# #     await conn.send(QuicStreamEvent(new_stream_id, list_request, False))
    
# #     # Receive and process responses
# #     while True:
# #         message = await conn.receive()
# #         if message.end_stream:
# #             break
# #         response = json.loads(message.data.decode('utf-8'))
# #         print('Server response:', response)

# # echo_client.py

# import json
# from aioquic.quic.events import StreamDataReceived, StreamDataSent, QuicEvent
# from collections import deque

# class EchoQuicConnection:
#     def __init__(self, connection):
#         self.connection = connection
#         self.received_data = deque()
    
#     async def new_stream(self):
#         return self.connection.get_next_available_stream_id()
    
#     async def send(self, event: StreamDataSent):
#         self.connection.send_stream_data(event.stream_id, event.data, end_stream=event.end_stream)
    
#     async def receive(self):
#         while True:
#             event = await self.connection.next_event()
#             if isinstance(event, StreamDataReceived):
#                 return event

# async def inventory_client_proto(conn: EchoQuicConnection):
#     new_stream_id = await conn.new_stream()
    
#     # Request to list all inventory items
#     list_request = json.dumps({'action': 'list'}).encode('utf-8')
#     await conn.send(StreamDataSent(new_stream_id, list_request, end_stream=True))
    
#     # Receive and process responses
#     event = await conn.receive()
#     if event.end_stream:
#         response = json.loads(event.data.decode('utf-8'))
#         print('Server response:', response)
#         return response


# echo_client.py

import json
from aioquic.quic.events import StreamDataReceived

class EchoQuicConnection:
    def __init__(self, connection):
        self.connection = connection
    
    async def new_stream(self):
        return self.connection.get_next_available_stream_id()
    
    async def send(self, stream_id, data, end_stream=False):
        self.connection.send_stream_data(stream_id, data, end_stream=end_stream)
    
    async def receive(self):
        while True:
            event = await self.connection.next_event()
            if isinstance(event, StreamDataReceived):
                if event.end_stream:
                    return event.data

async def inventory_client_proto(conn: EchoQuicConnection):
    new_stream_id = await conn.new_stream()
    
    # Request to list all inventory items
    list_request = json.dumps({'action': 'list'}).encode('utf-8')
    await conn.send(new_stream_id, list_request, end_stream=True)
    
    # Receive and process responses
    data = await conn.receive()
    response = json.loads(data.decode('utf-8'))
    print('Server response:', response)
    return response

