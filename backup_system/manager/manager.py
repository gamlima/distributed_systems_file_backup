from socket import *
import os

def receive_pass_file(connectionSocket, filename, serverSocket, server_address):
    serverSocket.sendall(filename.encode('utf-8'))
    response = serverSocket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")
    if response == 'READY':
        while True:
            bytes_read = connectionSocket.recv(1024)
            print(f"Received {len(bytes_read)} bytes. Enviando para servidor")  # Depuração
            serverSocket.sendall(bytes_read)
            if bytes_read.endswith(b'EOF'):
                print("Received EOF")
                break

managerPort = 9000
managerSocket = socket(AF_INET, SOCK_STREAM)
managerSocket.bind(('', managerPort))
managerSocket.listen(1)

print("The manager is ready to receive")

server_address = ('localhost', 9001) # Trocar pelo algoritmo de escolha
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.connect(server_address)

while True:
    connectionSocket, addr = managerSocket.accept()
    print(f"Connection from: {addr}")
    filename = connectionSocket.recv(1024).decode('utf-8') 
    print(f"Receiving file: {filename}")
    connectionSocket.sendall('READY'.encode('utf-8'))
    #Nesse ponto, chamar função para escolher servidor para envio
    #Em seguida, iniciar conexão com servidor de envio e repassar dados recebidos com a função chamada na linha seguinte (receive_pass_file)
    receive_pass_file(connectionSocket, filename, serverSocket, server_address)
    print("Request received and file sent to servers!")
    result = "Arquivo recebido e armazenado!".encode('utf-8')
    connectionSocket.send(result)
    connectionSocket.close()
