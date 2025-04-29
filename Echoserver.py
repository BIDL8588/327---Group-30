
import socket
from datetime import datetime, timedelta

metadata = {
    "fridge": {
        "device_id": "fridge",
        "type": "moisture",
        "timezone": "UTC",
        "unit": "percentage"  
    },
    "dishwasher": {
        "device_id": "dishwasher",
        "type": "water",
        "timezone": "UTC",
        "unit": "liters"
    },
    "fridge_2": {
        "device_id": "fridge_2",
        "type": "electricity",
        "timezone": "UTC",
        "unit": "kWh"
    }
}
def get_average_moisture(cursor):
    now = datetime.utcnow()
    start_time = now - timedelta(hours=3)
    cursor.execute("""
        SELECT value FROM fridge_kitchen_data
        WHERE reading_time >= ?
    """, (start_time.strftime("%Y-%m-%d %H:%M:%S"),))
    rows = cursor.fetchall()
    if rows:
        avg_moisture = sum([float(row[0]) for row in rows]) / len(rows)
        return round(avg_moisture, 2)
    return None
def p_query(query,cursor): 
    pass


###############TCP SET UP
HOST = '10.128.0.2' # local ip address
PORT = 4000 # port nuber to listen for incoming connections


#create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT)) #bind the socket to IP address and port
server_socket.listen(5) #listen for 5 connections

print(f"Server listening on {HOST}:{PORT}")

#accept an incoming connection from a client
client_socket, client_address = server_socket.accept() 
print(f"Connection established with {client_address}")
#loop to receive and process messages
while True:
    data = client_socket.recv(5000).decode('utf-8')#Receive data from client and decode it
    if not data:
        break 
    print(f"Received from client: {data}")
#process the data
    response = data.upper()
#send the processed response back to the client
    client_socket.send(response.encode('utf-8')) 
#close the client socket and the server socket 
client_socket.close()
server_socket.close()  
