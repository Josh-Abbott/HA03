import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\nReceived message: {message}")
        except:
            print("Connection lost.")
            break

def send_message(client_socket):
    while True:
        message = input("Enter message (/sendfile <filename> to send a file): ")
        if message.startswith("/sendfile"):
            filename = message.split()[1]
            if os.path.exists(filename):
                client_socket.send(message.encode())
                send_file(client_socket, filename)
            else:
                print(f"File {filename} not found.")
        else:
            client_socket.send(message.encode())

def send_file(client_socket, filename):
    print(f"Sending file: {filename}")

    file_size = os.path.getsize(filename)
    client_socket.send(str(file_size).encode('utf-8'))

    with open(filename, "rb") as f:
        while (data := f.read(1024)):
            client_socket.send(data)
            
    print(f"File {filename} sent successfully.")

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        send_thread = threading.Thread(target=receive_messages, args=(client,))
        send_thread.start()
        
        send_message(client)
    
if __name__ == "__main__":
    start_client()