import socket

valid_queries = [
    "What is the average moisture inside my kitchen fridge in the past three hours?",
    "What is the average water consumption per cycle in my smart dishwasher?",
    "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"
]

server_ip = input("Enter server IP address: ")
server_port = input("Enter server port: ")

try:
    server_port = int(server_port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
except (ValueError, socket.error) as e:
    print(f"Error: {e}")
    exit()

while True:
    print("\nPlease choose one of the following queries by entering the corresponding number:")
    for idx, query in enumerate(valid_queries, start=1):
        print(f"{idx}. {query}")

    choice = input("\nEnter the number of your query (or type 'exit' to quit): ").strip()

    if choice.lower() == 'exit':
        client_socket.send(b'exit')  
        break

    try:
        choice = int(choice)
        if choice < 1 or choice > len(valid_queries):
            print("Invalid choice, please select a number from the available options.")
            continue
        message = valid_queries[choice - 1]
        client_socket.send(message.encode('utf-8'))

        response = client_socket.recv(4096).decode('utf-8')
        print(f"Server Response: {response}")
    
    except ValueError:
        print("Invalid input, please enter a valid number corresponding to the query.")

client_socket.close()
