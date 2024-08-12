from socket import *
import os
import select

def send_replica(replica_addr, filename):
    replica_ip, replica_port = replica_addr.split(':')
    replica_port = int(replica_port)
    replicaSocket = socket(AF_INET, SOCK_STREAM)
    replicaSocket.connect((replica_ip, replica_port))

    directory = './storage_files'
    filepath = os.path.join(directory, filename)
    replicaSocket.sendall("REPLICA".encode('utf-8'))
    response = replicaSocket.recv(1024).decode('utf-8')
    if response == 'READY':
        replicaSocket.sendall(os.path.basename(filename).encode('utf-8'))
        response = replicaSocket.recv(1024).decode('utf-8')
        print(f"Replica server response: {response}")
        if response == 'READY':
            with open(filepath, 'rb') as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    print(f"Sending {len(bytes_read)} bytes")  # Depuração
                    replicaSocket.sendall(bytes_read)
            replicaSocket.sendall(b'EOF')
            print("Sent EOF")
            response = replicaSocket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
            if response == 'READY FOR REPLICA':
                replicaSocket.sendall('NO REPLICA'.encode('utf-8'))
        replicaSocket.close()

def receive_file(connection, filename):
    directory = './storage_files'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    print(f"Criando arquivo {filename} nesse servidor")
    with open(filepath, 'wb') as f:
        while True:
            bytes_read = connection.recv(1024)
            #if bytes_read.endswith(b'EOF'):
                #f.write(bytes_read[:-3])  # Escreve os dados excluindo 'EOF'
                #print("Received EOF")
                #break
            if b'EOF' in bytes_read:
                f.write(bytes_read[:bytes_read.index(b'EOF')])
                print(f"Received {len(bytes_read)} bytes")  # Depuração
                print("Received EOF marker")
                break
            print(f"Received {len(bytes_read)} bytes")  # Depuração
            f.write(bytes_read)
        print(f"File {filename} has been saved to {filepath}")
        
    #Utilizar essa parte apenas quando atualizar o manager.  Lembrar de atualizar o server2 também.
    connection.sendall('READY FOR REPLICA'.encode('utf-8'))
    replica_addr = connection.recv(1024).decode('utf-8')
    print(f"Replica address: {replica_addr}")
    if replica_addr != 'NO REPLICA':
        send_replica(replica_addr, filename)

def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

serverPort = 9002
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection from: {addr}")
    command = connectionSocket.recv(1024).decode('utf-8')
    print(f"Comando atual: {command}")
    if command == "LATENCY":
        print("Toma aí minha latência")
    elif command == "STORAGE":
        print("Ta vendo meu armazenamento né")
        directory = './storage_files'
        total_size = get_directory_size(directory)
        connectionSocket.sendall(str(total_size).encode('utf-8'))
    else:
        connectionSocket.sendall('READY'.encode('utf-8'))
        print("Bora fazer backup")
        filename = connectionSocket.recv(1024).decode('utf-8')
        print(f"Receiving file: {filename}")
        connectionSocket.sendall('READY'.encode('utf-8'))
        receive_file(connectionSocket, filename)
        print("Request received!")
        result = "Arquivo recebido e armazenado!".encode('utf-8')
        connectionSocket.send(result)
        connectionSocket.close()