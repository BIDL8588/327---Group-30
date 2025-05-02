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
    for idx, query in enumerate(valid_queries, start=1):
        print(f"{idx}. {query}")

    
   try:
        choice = int(input("\nEnter the number of your query (or type 'exit' to quit): ").strip())
        
        if choice == "exit":
            break
        if choice < 1 or choice > len(valid_queries):
            print("Invalid choice, please select a number from the available options.")
            continue

        message = valid_queries[choice - 1]  
        client_socket.send(message.encode('utf-8')) 

        response = ''
        while True:
            chunk = client_socket.recv(1024).decode('utf-8')  
            if not chunk:
                break
            response += chunk
        print(f"Server Response: {response}")
    
    except ValueError:
        print("Invalid input, please enter a number corresponding to the query.")

client_socket.close()
