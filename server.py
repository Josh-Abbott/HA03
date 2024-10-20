import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
clients = []

def broadcast(message, source_client):
    for client in clients:
        if client != source_client:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket, client_address):
    print(f"Connected to {client_address}")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message.startswith("/sendfile"):
                filename = message.split()[1]
                receive_file(client_socket, filename)
            else:
                print(f"Received message from {client_address}: {message}")
                broadcast(message, client_socket)
        except:
            break     

    print(f"Connection with {client_address} ended.")
    client_socket.close()
    clients.remove(client_socket)     
            
def receive_file(client_socket, filename):
    print(f"Receiving file: {filename}")

    file_size = int(client_socket.recv(1024).decode('utf-8'))

    received_size = 0
    with open(f"server_{filename}", "wb") as f:
        while received_size < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
            received_size += len(data)

    print(f"File {filename} received successfully.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()