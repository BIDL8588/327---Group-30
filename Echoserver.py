import socket
import psycopg2
from datetime import datetime, timedelta, timezone

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
        "unit": "percentage",
        "sensor_key": "DHT11 - DHT11-moisture",
        "table": "Fridge_virtual"
    },
    "dishwasher": {
        "device_id": "9e729bba-71f8-44f4-9fb8-db7842e121cf",
        "type": "water",
        "timezone": "UTC",
        "unit": "liters",
        "sensor_key": "YF-S201 - YFS201-Water",
        "table": "Dishwasher_virtual"
    },
    "fridge_2": {
        "device_id": "fe97fda9-9b5f-48ae-84dc-f9826711edef",
        "type": "electricity",
        "timezone": "UTC",
        "unit": "kWh"
    }
}

def get_moisture(cursor):
    metadata_entry = metadata["fridge"]
    table = metadata_entry["table"]
    sensor_key = metadata_entry["sensor_key"]
    time_limit = datetime.utcnow() - timedelta(hours=3)

    query = f"""
        SELECT AVG((payload->>'{sensor_key}')::float)
        FROM {table}
        WHERE time >= %s
    """
    cursor.execute(query, (time_limit,))
    result = cursor.fetchone()

    if result and result[0] is not None:
        avg_moisture = round(result[0], 2)
        return f"The average moisture inside kitchen fridge in the past three hours is {avg_moisture} % RH."
    else:
        return "No moisture data available in the past three hours."






def get_average_water_usage(cursor):
    sensor_key = metadata["dishwasher"]["sensor_key"]
    table = metadata["dishwasher"]["table"]
    time_limit = datetime.now(timezone.utc) - timedelta(days=1)

    cursor.execute(f"""
        SELECT AVG((payload->>%s)::float)
        FROM {table}
        WHERE time >= %s
    """, (sensor_key, time_limit))
    
    result = cursor.fetchone()
    if result and result[0] is not None:
        avg_liters = result[0]
        avg_gallons = round(avg_liters * 0.264172, 2)
        return f"The average water consumption per cycle is {avg_gallons} gallons."
    else:
        return "No dishwasher water usage data available."

def electricity(cursor):
    usage = {}
    for device in ["fridge", "dishwasher", "fridge_2"]:
        device_id = metadata[device]["device_id"]
        cursor.execute("""
            SELECT SUM(energy_used) FROM device_data
            WHERE device_id = %s
        """, (device_id,))
        result = cursor.fetchone()
        usage[device] = result[0] if result[0] is not None else 0

    most_elec = max(usage, key=usage.get)
    kwh = round(usage[most_elec], 2)
    return f"{most_elec} consumed the most electricity: {kwh} kWh."

def p_query(query, cursor): 
    query = query.lower()
    if "average moisture" in query:
        return get_moisture(cursor)
    elif "average water" in query:
        return get_average_water_usage(cursor)
    elif "consumed more electricity" in query:
        return electricity(cursor)
    else:
        return ("Sorry, this query cannot be processed. Please try one of the following:\n"
                "1. What is the average moisture inside my kitchen fridge in the past three hours?\n"
                "2. What is the average water consumption per cycle in my smart dishwasher?\n"
                "3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?")

############### TCP SETUP
HOST = '10.128.0.2'
PORT = 4000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

client_socket, client_address = server_socket.accept() 
print(f"Connection established with {client_address}")

conn = database_conn()
if not conn:
    client_socket.send(b"Database connection failed.")
    client_socket.close()
    server_socket.close()
    exit()

cursor = conn.cursor()

try:
    while True:
        data = client_socket.recv(5000).decode('utf-8')
        if not data:
            break 
        print(f"Received from client: {data}")
        response = p_query(data, cursor)
        client_socket.send(response.encode('utf-8')) 
finally:
    cursor.close()
    conn.close()
    client_socket.close()
    server_socket.close()
