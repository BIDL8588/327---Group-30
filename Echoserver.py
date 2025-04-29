
import socket
from datetime import datetime, timedelta


DB_CONFIG = {
    'url': "postgresql://neondb_owner:npg_wnz8jmce2qHh@ep-bitter-pine-a539fzen-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
}
def database_conn():
    try:
        conn = psycopg2.connect(DB_CONFIG['url'], sslmode="require")
        print("Connected to Neon successfully.")
        return conn
    except Exception as e:
        print(f"Error connecting to Neon: {e}")
        return None


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
def get_moisture(): 
    device_id = "fridge"
    
    
    pass
    
##not official function
def get_average_water_usage(cursor):
    device_id = "dishwasher"

    cursor.execute("""
        SELECT AVG(water_used) FROM dishwasher_cycles
        WHERE device_id = %s
    """, (device_id,))
    result = cursor.fetchone()

    if result and result[0] is not None:
        avg_liters = result[0]
        avg_gallons = avg_liters * 0.264172
        avg_gallons = round(avg_gallons, 2)
        return f"The average water consumption per cycle is {avg_gallons} gallons."
    else:
        return "No dishwasher water usage data available."
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
