from socket import *
import os
import time

def delete_file(filename):
    directory = './storage_files'
    filepath = os.path.join(directory, filename)
    os.remove(filepath)
    print(f"Arquivo '{filename}' excluído com sucesso.")

def send_replica(replica_addr, filename):
    replica_ip, replica_port = replica_addr.split(':')
    replica_port = int(replica_port)
    replicaSocket = socket(AF_INET, SOCK_STREAM)
    replicaSocket.connect((replica_ip, replica_port))

    directory = './storage_files'
    filepath = os.path.join(directory, filename)
    replicaSocket.sendall("REPLICA".encode('utf-8'))
    response = replicaSocket.recv(1024).decode('utf-8')
    if response == 'READY FOR REPLICA':
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
            if b'EOF' in bytes_read:
                f.write(bytes_read[:bytes_read.index(b'EOF')])
                print(f"Received {len(bytes_read)} bytes")  # Depuração
                print("Received EOF marker")
                connection.sendall('EOF RECEIVED'.encode('utf-8'))
                print("Sent EOF RECEIVED")  # Adicionado para depuração
                break
            print(f"Received {len(bytes_read)} bytes")  # Depuração
            f.write(bytes_read)
        print(f"File {filename} has been saved to {filepath}")
        #connection.sendall('FILE RECEIVED AND STORED'.encode('utf-8'))
        time.sleep(2)

def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

serverPort = 9003
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
ip_replica_1 = 'VAZIO'
ip_replica_2 = 'VAZIO'

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
        print(f"Total_size = {total_size}")
        connectionSocket.sendall(str(total_size).encode('utf-8'))
    elif command == 'IP FOR REPLICA':
        print("Recebendo IP para envio de réplica")
        connectionSocket.sendall('READY'.encode('utf-8'))
        ip_replica_1 = connectionSocket.recv(1024).decode('utf-8')
        connectionSocket.sendall('IP 1 recebido'.encode('utf-8'))
        print("Ip para replica  1 recebido")
        ip_replica_2 = connectionSocket.recv(1024).decode('utf-8')
        connectionSocket.sendall('IP 2 recebido'.encode('utf-8'))
        print("Ip para replica  2 recebido")
    elif command == 'REPLICA':
        connectionSocket.sendall('READY FOR REPLICA'.encode('utf-8'))
        filename = connectionSocket.recv(1024).decode('utf-8')
        print("Recebendo o nome do arquivo para rplica")
        connectionSocket.sendall('READY'.encode('utf-8'))
        print("Recebendo uma replica")
        receive_file(connectionSocket, filename)
        print("Replica recebida com sucesso!")
    else:
        connectionSocket.sendall('READY'.encode('utf-8'))
        print("Bora fazer backup")
        filename = connectionSocket.recv(1024).decode('utf-8')
        print(f"Receiving file: {filename}")
        connectionSocket.sendall('READY FOR RECEIVE'.encode('utf-8'))
        receive_file(connectionSocket, filename)
        time.sleep(2)
        print(ip_replica_1)
        time.sleep(2)
        print(ip_replica_2)
        time.sleep(2)
        if ip_replica_1 != 'VAZIO':
            send_replica(ip_replica_1, filename)
            send_replica(ip_replica_2, filename)
            delete_file(filename)
        ip_replica_1 = 'VAZIO'
        ip_replica_2 = 'VAZIO'