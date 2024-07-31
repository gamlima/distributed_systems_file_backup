from socket import *
import os

def receive_file(connection, filename):
    directory = './storage_files'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as f:
        while True:
            bytes_read = connection.recv(1024)
            if bytes_read.endswith(b'EOF'):
                f.write(bytes_read[:-3])  # Escreve os dados excluindo 'EOF'
                print("Received EOF")
                break
            print(f"Received {len(bytes_read)} bytes")  # Depuração
            f.write(bytes_read)
    print(f"File {filename} has been saved to {filepath}")

serverPort = 9001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection from: {addr}")
    filename = connectionSocket.recv(1024).decode('utf-8') 
    print(f"Receiving file: {filename}")
    connectionSocket.sendall('READY'.encode('utf-8'))
    receive_file(connectionSocket, filename)
    print("Request received!")
    result = "Arquivo recebido e armazenado!".encode('utf-8')
    connectionSocket.send(result)
    connectionSocket.close()
