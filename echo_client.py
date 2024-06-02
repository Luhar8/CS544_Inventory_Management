
# echo_client.py

from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu
import time
import json
from tabulate import tabulate

async def inventory_client_proto(scope, conn: EchoQuicConnection):
    print("Welcome to Inventory Management Tool.")
    # Initial inventory fetch
    try:
        qim = pdu.QueryInventoryMessage(1, 12345, int(time.time()), )
        initial_stream_id = conn.new_stream()
        print("[cli] Sending initial inventory request")
        await conn.send(QuicStreamEvent(initial_stream_id, qim.to_bytes(), False))

        table = []
        headers = ["Item Number", "Item Name", "Quantity"]

        # Receive and display initial inventory
        while True:
            message = await conn.receive()
            if message.end_stream:
                print('[cli] Received initial inventory items from server')
                break
            irm = pdu.InventoryResponseMessage.from_bytes(message.data)
            table.append([irm.itemID, irm.itemName, irm.quantity])
        print(tabulate(table, headers, tablefmt="grid"))

        # Interaction loop for updates
        while True:
            response= input("[cli] Do you want to update the quantity of any item? (y/n): ").lower()
            if response == "y":
                item_id = int(input("Enter the Item ID to update: "))
                new_quantity = int(input("Enter the new quantity: "))
                if new_quantity<0:
                    print("[cli] Quantity cannot be negative, instead it is saved as 0")
                    new_quantity=0
                # Create a new stream for the update request
                update_stream_id = conn.new_stream()
                update_message = pdu.UpdateInventoryMessage(1, item_id, new_quantity).to_bytes()
                print("[cli] Sending update request")
                await conn.send(QuicStreamEvent(update_stream_id, update_message, False))

                # Clear the table for updated display
                table.clear()
                print("Fetching updated inventory...")

                # Receive and display updated inventory
                while True:
                    message = await conn.receive()
                    if message.end_stream:
                        print('[cli] Received updated inventory from server')
                        break
                    irm = pdu.InventoryResponseMessage.from_bytes(message.data)
                    table.append([irm.itemID, irm.itemName, irm.quantity])
                print(tabulate(table, headers, tablefmt="grid"))

            elif response =='n':
                print("Thank you for using the inventory management system!")
                break
            else:
                print("Invalid input. Please enter y or n.")
                continue
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the connection is closed properly
        print("Closing the connection...")
        await conn.close()