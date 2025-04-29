import socket

valid_queries = ["What is the average moisture inside my kitchen fridge in the past three hours?",
    "What is the average water consumption per cycle in my smart dishwasher?",
    "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"]
#user input for server IP address and port
server_ip = input("Enter server IP address:")
server_port = input("Enter server port:")

try:
    server_port = int(server_port) # turns the user input from string to integer just in case its a string
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creates TCP socket
    client_socket.connect((server_ip, server_port))#connects the client socket to server IP and port
except (ValueError, socket.error) as e:
    print(f"Error: {e}")
    exit()


while True:
    print("\nPlease choose one of the following queries:")
    for query in valid_queries:
        print(f"- {query}")

    
    message = input("\nEnter your query(or type 'exit' to quit): ").strip()# prompt user to enter message
    if message.lower() == "exit":
        break

    if message not in valid_queries: 
        print("\n Sorry, this query can't be processed.")
        print("Please try one of the following valid queries:")
        for query in valid_queries:
            print(f"- {query}")
        continue
    client_socket.send(message.encode('utf-8'))#send the message to the server encoding it
    response = client_socket.recv(1024).decode('utf-8')# receive the response form the server and decode it
    print(f"Server Response: {response}")

client_socket.close()
