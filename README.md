# Inventory Management System

Our team (Rahul Bolineni, Shreya Laheri, Apurva Deshpande) developed an Inventory Management System for a grocery store, implementing the QUIC protocol. This application allows users to add, edit, or delete inventory items.

## Features
- **Add Inventory Item**
- **Edit Inventory Item**
- **Delete Inventory Item**

## SSL Certificates
We generated new SSL certificates (`quic_certificate.pem`) and a key (`quic_private_key.pem`) for this application using the `sam.cnf` configuration file. You can find the files in cert directory.

## Message Definitions
We implemented the message definitions as described in the project proposal, including:
- **UpdateInventoryMessage**
- **DeleteInventoryMessage**
- **AddInventoryMessage**

## Setup and Execution

Follow the steps below to set up and run the application:

### Prerequisites
- Install the latest version of Python

### Steps

1. **Download and Unzip the Application**
   - Clone the repository from GitHub and unzip the file.

2. **Create a Virtual Environment**
   - Navigate to the project directory and create a virtual environment:
     ```sh
     python3 -m venv venv
     ```

3. **Activate the Virtual Environment**
   - Activate the virtual environment:
     ```sh
     source venv/bin/activate
     ```

4. **Install Dependencies**
   - Install the required dependencies using pip (or pip3 on some systems):
     ```sh
     pip3 install -r requirements.txt
     ```

5. **Run the Server**
   - Start the server before executing the client:
     ```sh
     (.venv) rahul@Rahuls-MBP CS544 % python3 echo.py server
     [svr] Server starting...
     ```

6. **Run the Client**
   - Open a new terminal and execute the client.Make sure the client terminal is in virtual environment by following above steps. This will establish the connection between the client and server:
     ```sh
     (.venv) rahul@Rahuls-MBP CS544 % python3 echo.py client

     ```
   - The user credentials for the application is
      - For Admin (Can View, Add, Update, Delete)
         - Email: admin@example.com
         - Password: adminpassword
      - For Client (Only View)
         - Email: client@example.com
         - Passowrd: clientpassword
   - The client output should look like this:
     ```sh
      Welcome to Inventory Management Tool.
      Enter your email: admin@example.com
      Enter your password: adminpassword
      [cli] Sending initial inventory request
      [cli] Received initial inventory items from server
      +---------------+-------------+------------+
      |   Item Number | Item Name   |   Quantity |
      +===============+=============+============+
      |           101 | Apples      |         50 |
      +---------------+-------------+------------+
      |           102 | Whole Milk  |         75 |
      +---------------+-------------+------------+
      |           103 | Coffee      |         25 |
      +---------------+-------------+------------+
      |           104 | Yogurt      |         30 |
      +---------------+-------------+------------+
      [cli] Select an action - Update (u), Delete (d), Add(a), View Log(v), Exit (e):
     ```

### Usage
- Follow the on-screen prompts to update, delete, or add inventory items.
- To exit the client application, select the `Exit (e)` option.

### Stopping the Server
- To stop the server, use `Ctrl+C` in the server terminal to trigger a keyboard interruption.

## Notes
- Ensure that the server is running before starting the client.
- All operations (add, update, delete) will reflect in the inventory list after each action.

## Youtube Link
Below is the youtube link describing about project: https://youtu.be/qtuT_YFrgF8
