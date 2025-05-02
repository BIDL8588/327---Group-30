
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
        "device_id": "89t-yx1-9k7-s46",
        "type": "moisture",
        "timezone": "UTC",
        "unit": "percentage"  
    },
    "dishwasher": {
        "device_id": "7a80c32e-90a0-49fc-90d1-4dd669e8f886",
        "type": "water",
        "timezone": "UTC",
        "unit": "liters"
    },
    "fridge_2": {
        "device_id": "bac88fe2-92b4-4a6f-8a4f-df8d627a1255",
        "type": "electricity",
        "timezone": "UTC",
        "unit": "kWh"
    }
}
def get_moisture(cursor): 
    device_id = metadata["fridge"]["device_id"]
    time_limit = date.time.utcnow() - timedelta(hours = 3)
    
    cursor.execute(""" 
    SELECT AVG(moisture) FROM fridge_data
    WHERE device_id = %s AND timestamp >= %s
    """, (device_id, time_limit))
    result = cursor.fetchone()

if result and result[0] is not None: 
    avg_moisture = round(result[0], 2)
    return f"The average moisture inside kitchen fridge in the past three hours is {avg_moisture} % RH."
else:
    return "No moisture data available in the past three hours."

##not official function
def get_average_water_usage(cursor):
    device_id = metadata["fridge"]["device_id"]

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

def electricity(cursor):
    usage = {}

    for device in ["fridge", "diswasher", "fridge_2"]: 
        cursor.execute("""
            SELECT SUM(energy_used) FROM device_data
            WHERE device_id = %s
        """, (device_id,))
        result = cursor.fetchone()
        usage [device] = result[0] if result[0] is not None else 0

    most_elec = max(usage, key = usage.get)
    kwh = round(usage[most_elec],2)
    return f"{most_elec} consumed the most elecricity: {kwh} kwh."

        
def p_query(query,cursor): 
    query = query.lower()

    if "average moisture" in query:
        return get_average_moisture(cursor)
    elif "average water" in query:
        return get_average_water_usage(cursor)
    elif "consumed more electricity" in query:
        return compare_electricity(cursor)
    else:
        return ("Sorry, this query cannot be processed. Please try one of the following:\n"
                "1. What is the average moisture inside my kitchen fridge in the past three hours?\n"
                "2. What is the average water consumption per cycle in my smart dishwasher?\n"
                "3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?")


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
