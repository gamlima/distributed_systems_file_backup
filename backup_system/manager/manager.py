from socket import *
import os
import time

def update_servers_latency(servers_info):
    for server in servers_info:
        serverSocket = socket(AF_INET, SOCK_STREAM)
        start_time = time.time()
        serverSocket.connect(server['address'])
        serverSocket.sendall("LATENCY".encode('utf-8'))
        server['latency'] = time.time() - start_time
        print(server['latency'])
        serverSocket.close()

def update_servers_storage(servers_info):
    for server in servers_info:
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.connect(server['address'])
        serverSocket.sendall("STORAGE".encode('utf-8'))
        response = serverSocket.recv(1024).decode('utf-8')
        if response != None:
            server['storage'] = int(response)
            print(f"storage: {server['storage']}")
        serverSocket.close()

def choose_server(servers_info):
    print("Bora escolher os melhores servers")
    update_servers_latency(servers_info)
    print("Consegui atualizar as latências")
    print("Bora analisar os storages")
    update_servers_storage(servers_info)
    print("Consegui atualizar os storages")
    #Verificar casos específicos de armazenamento ou latencia igual a 0 ou infinito, ou cheio
    best_storage = min(server['storage'] for server in servers_info)
    print(f"Melhor storage: {best_storage}")
    best_latency = min(server['latency'] for server in servers_info) 
    print(f"Melhor latência: {best_latency}")

    def score(server):
        if server['storage'] == 0:
            normalized_storage = 1
        else:
            normalized_storage = best_storage / server['storage'] #Tratar divisão por zero
        normalized_latency = 1
        if server['latency'] == 0:
            normalized_latency = 1
        else:
            normalized_latency = best_latency / server['latency']
        # Peso para as métricas: ajuste conforme necessário
        return 0.5 * normalized_storage + 0.5 * normalized_latency

    sorted_servers = sorted(servers_info, key=score, reverse=True)
    return sorted_servers[:3]

servers_info = [
    {'address': ('localhost', 9001), 'storage': 1000, 'latency': 1},
    {'address': ('localhost', 9002), 'storage': 1000, 'latency': 1},
    {'address': ('localhost', 9003), 'storage': 1000, 'latency': 1},
    {'address': ('localhost', 9004), 'storage': 1000, 'latency': 1}
]

managerPort = 9000
managerSocket = socket(AF_INET, SOCK_STREAM)
managerSocket.bind(('', managerPort))
managerSocket.listen(1)

print("The manager is ready to receive")

while True:
    connectionSocket, addr = managerSocket.accept()
    print(f"Connection from: {addr}")
    connectionSocket.recv(1024).decode('utf-8')

    best_servers = choose_server(servers_info)
    main_server, replica_server1, replica_server2 = best_servers[0]["address"], best_servers[1]["address"], best_servers[2]["address"]
    
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.connect(main_server)
    serverSocket.sendall('IP FOR REPLICA'.encode('utf-8'))
    response = serverSocket.recv(1024).decode('utf-8')
    if response == 'READY':
        str_replica_server1 = ':'.join(map(str, replica_server1))
        serverSocket.sendall(str_replica_server1.encode('utf-8'))
        print("Enviando IP 1 de réplica para o servidor principal")
        response = serverSocket.recv(1024).decode('utf-8')
        if response == 'IP 1 recebido':
            str_replica_server2 = ':'.join(map(str, replica_server2))
            serverSocket.sendall(str_replica_server2.encode('utf-8'))
            print("Enviando IP 2 de réplica para o servidor principal")
            response = serverSocket.recv(1024).decode('utf-8')
    serverSocket.close()

    str_main_server = ':'.join(map(str, main_server))
    connectionSocket.sendall(str_main_server.encode('utf-8'))