# echo_client.py
from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu
import time
import json
from tabulate import tabulate

# Define hardcoded user credentials along with roles
users = {
    "admin@example.com": {"password": "adminpassword", "role": "admin"},
    "client@example.com": {"password": "clientpassword", "role": "client"}
}

# Define authentication function to return email and role
def authenticate_user():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    if email in users and users[email]["password"] == password:
        return email, users[email]["role"]
    else:
        print("Invalid email or password. Please try again.")
        return None, None

# Initialize item_ids
item_ids = []

# Define inventory_client_proto function
async def inventory_client_proto(scope, conn: EchoQuicConnection):
    print("Welcome to Inventory Management Tool.")
    # Authenticate user
    email, role = authenticate_user()
    if not email:
        print("Authentication failed. Exiting...")
        return

    # Initial inventory fetch and interaction loop for viewing inventory and audit log
    try:
        # Initial inventory fetch
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
            item_ids.append(irm.itemID)
        print(tabulate(table, headers, tablefmt="grid"))

        # Interaction loop based on user role
        if role == "admin":
            while True:
                response = input("[cli] Select an action - Update (u), Delete (d), Add(a), View Log(v), Exit (e): ").lower()
                if response == "u":
                    update_stream_id = await update_item(conn, item_ids)
                    if update_stream_id is not None:
                        await display_updated_inventory(conn, update_stream_id)
                elif response == "d":
                    delete_stream_id = await delete_item(conn, item_ids)
                    if delete_stream_id is not None:
                        await display_updated_inventory(conn, delete_stream_id)
                elif response == "a":
                    add_stream_id = await add_item(conn, item_ids)
                    if add_stream_id is not None:
                        await display_updated_inventory(conn, add_stream_id)
                elif response == "v":
                    await view_audit_log(conn)
                elif response == "e":
                    print("Thank you for using the inventory management system!")
                    break
                else:
                    print("Invalid input. Please choose 'u', 'd', 'a', 'v' or 'e'.")
                    continue
        else:
            while True:
                response = input("[cli] Select an action - View Log(v), Exit (e): ").lower()
                if response == "v":
                    await view_audit_log(conn)
                elif response == "e":
                    print("Thank you for using the inventory management system!")
                    break
                else:
                    print("Invalid input. Please choose 'v' or 'e'.")
                    continue
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the connection is closed properly
        print("Closing the connection...")
        await conn.close()

async def display_updated_inventory(conn, stream_id):
    table = []
    headers = ["Item Number", "Item Name", "Quantity"]
    item_ids.clear()
    print("Fetching updated inventory...")
    while True:
        message = await conn.receive()
        if message.end_stream:
            break
        irm = pdu.InventoryResponseMessage.from_bytes(message.data)
        table.append([irm.itemID, irm.itemName, irm.quantity])
        item_ids.append(irm.itemID)
    print(tabulate(table, headers, tablefmt="grid"))

async def update_item(conn, item_ids):
    item_id = int(input("Enter the Item ID to update: "))
    if item_id not in item_ids:
        print("You entered a wrong item ID. Please try again.")
        return
    new_quantity = int(input("Enter the new quantity: "))
    if new_quantity < 0:
        print("[cli] Quantity cannot be negative, instead it is saved as 0")
        new_quantity = 0
    update_stream_id = conn.new_stream()
    update_message = pdu.UpdateInventoryMessage(1, item_id, new_quantity).to_bytes()
    print("[cli] Sending update request")
    await conn.send(QuicStreamEvent(update_stream_id, update_message, False))
    return update_stream_id

async def delete_item(conn, item_ids):
    item_id = int(input("Enter the Item ID to delete: "))
    if item_id not in item_ids:
        print("You entered a wrong item ID. Please try again.")
        return
    delete_stream_id = conn.new_stream()
    delete_message = pdu.DeleteInventoryMessage(1, item_id).to_bytes()
    print("[cli] Sending delete request")
    await conn.send(QuicStreamEvent(delete_stream_id, delete_message, False))
    return delete_stream_id

async def add_item(conn, item_ids):
    item_id = int(input("Enter the Item ID to add: "))
    if item_id in item_ids:
        print("The Item ID already existed, enter a different one")
        return
    item_name = input("Enter the Item name: ")
    item_quantity = int(input("Enter the item quantity(>=0): "))
    if item_quantity<0:
        print("Item Quantity cannot be less than 0. Try entering correct value")
        return
    add_stream_id = conn.new_stream()
    add_message = pdu.AddInventoryMessage(1, item_id, item_name, item_quantity).to_bytes()
    print("[cli] Sending Add request")
    await conn.send(QuicStreamEvent(add_stream_id, add_message, False))
    print(f"[cli] Added new item {item_name} with ID {item_id} and quantity {item_quantity}")
    return add_stream_id

async def view_audit_log(conn):
    log_stream_id = conn.new_stream()
    log_request_message = json.dumps({'type': 'audit_log'}).encode('utf-8')
    print("[cli] Sending audit log request")
    await conn.send(QuicStreamEvent(log_stream_id, log_request_message, False))
    print("Fetching audit log...")
    log_data = ""
    while True:
        message = await conn.receive()
        log_data += message.data.decode('utf-8')
        if message.end_stream:
            break
    print(log_data)
