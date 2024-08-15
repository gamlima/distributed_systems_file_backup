from socket import *
import time

def update_servers_latency(servers_info):
    for server in servers_info:
        serverSocket = socket(AF_INET, SOCK_STREAM)
        start_time = time.time()
        serverSocket.connect(server['address'])
        serverSocket.sendall("LATENCY".encode('utf-8'))
        server['latency'] = time.time() - start_time
        print(f"latency: {server['latency']}")
        serverSocket.close()

def update_servers_storage(servers_info):
    for server in servers_info:
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.connect(server['address'])
        serverSocket.sendall("STORAGE".encode('utf-8'))
        response = serverSocket.recv(1024).decode('utf-8')
        server['storage'] = int(response)
        print(f"storage: {server['storage']}")
        serverSocket.close()

def choose_server(servers_info):
    update_servers_latency(servers_info)
    update_servers_storage(servers_info)

    all_storages = [server['storage'] for server in servers_info if server['storage'] > 0]
    best_storage = min(all_storages) if all_storages else float('inf')
    all_latencies = [server['latency'] for server in servers_info if server['latency'] > 0]
    best_latency = min(all_latencies) if all_latencies else float('inf')

    def score(server):
        if server['storage'] == 0:
            normalized_storage = 1
        else:
            normalized_storage = (best_storage - server['storage']) / best_storage

        if server['latency'] == 0:
            normalized_latency = 1
        else:
            normalized_latency = (best_latency - server['latency']) / best_latency

        #Reajustar o peso das métricas se quiser
        return 0.5 * normalized_storage + 0.5 * normalized_latency

    sorted_servers = sorted(servers_info, key=score, reverse=True)
    return sorted_servers[:3]

servers_info = [
    {'address': ('localhost', 9001), 'storage': 0, 'latency': 0},
    {'address': ('localhost', 9002), 'storage': 0, 'latency': 0},
    {'address': ('localhost', 9003), 'storage': 0, 'latency': 0},
    {'address': ('localhost', 9004), 'storage': 0, 'latency': 0}
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