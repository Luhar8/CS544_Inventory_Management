from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import asyncio
from quic_engine import build_client_quic_config, AsyncQuicServer, connect, client_run, build_client_quic_configuration
from echo_client import EchoQuicConnection, inventory_client_proto
from flask import Flask, render_template, jsonify
import asyncio
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from echo_client import inventory_client_proto, EchoQuicConnection

app = Flask(__name__)
app.secret_key= 'super3'  # Change this to a random secret key for production

# Configuration for QUIC client
QUIC_SERVER = 'localhost'
QUIC_PORT = 4433
quic_config = build_client_quic_config()
cert_file='./cert/quic_certificate.pem'


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         # Placeholder for authentication logic
#         if username == "admin" and password == "password":  # Simplified check for demonstration
#             session['logged_in'] = True
#             return redirect(url_for('inventory'))
#         else:
#             return render_template('login.html', error='Invalid credentials')
#     return render_template('login.html')
@app.route('/')
@app.route('/inventory')
def inventory():
    config = build_client_quic_config(cert_file)
    # asyncio.run(run_client(QUIC_SERVER, QUIC_PORT, config))

    # inventory_data = asyncio.run(fetch_inventory_data())
    # print(inventory_data)  # Debugging line to check the structure of inventory_data
    # return render_template('inventory.html', inventory=inventory_data)
    # async def get_inventory():
    #     async with connect(QUIC_SERVER, QUIC_PORT, config) as conn:
    #         echo_conn = EchoQuicConnection(conn)
    #         return await inventory_client_proto(echo_conn)

    # inventory_data = asyncio.run(get_inventory())
    # return render_template('inventory.html', inventory=inventory_data)
    config = build_client_quic_configuration(cert_file)

    inventory_data = asyncio.run(client_run(config))
    return render_template('inventory.html', inventory=inventory_data)

async def fetch_inventory_data():
    inventory_data = {'items': []}
    print("client request accepted")
    try:
        async with connect(QUIC_SERVER, QUIC_PORT, configuration=quic_config, create_protocol=AsyncQuicServer) as client:
            await client.wait_connected()
            inventory_data = await client._client_handler.fetch_inventory()
    except Exception as e:
        print(f"Failed to fetch inventory data: {e}")
    return inventory_data

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    item_id = request.json['item_id']
    operation = request.json['operation']  # 'increase' or 'decrease'
    asyncio.run(send_quic_update(item_id, operation))
    return jsonify({"status": "success"})

async def send_quic_update(item_id, operation):
    try:
        async with connect(QUIC_SERVER, QUIC_PORT, configuration=quic_config, create_protocol=AsyncQuicServer) as client:
            await client.wait_connected()
            update_command = {'item_id': item_id, 'operation': operation}
            await client._client_handler.launch_echo(update_command)
    except Exception as e:
        print(f"Failed to send update via QUIC: {e}")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
