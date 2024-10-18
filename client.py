import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 12345

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
            received_message = client_socket.recv(1024).decode('utf-8')
            if not received_message:
                break
            print(f"Received message: {received_message}")

def send_file(client_socket, filename):
    print(f"Sending file: {filename}")
    with open(filename, "rb") as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            client_socket.send(data)
    print(f"File {filename} sent successfully.")

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        send_thread = threading.Thread(target=send_message, args=(client,))
        send_thread.start()
        send_thread.join()
    
if __name__ == "__main__":
    start_client()