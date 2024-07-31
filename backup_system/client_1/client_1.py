import socket
import os
import time

def clean_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def client_menu():
    clean_screen()
    print(" --------------------------------------- ")
    print("|           SISTEMA DE BACKUP           |")
    print("|---------------------------------------|")
    print("|     Enviar arquivo    - Digite 1      |")
    print("|     Recuperar arquivo - Digite 2      |")
    print("|     Excluir arquivo   - Digite 3      |")
    print("|     Fechar sistema    - Digite 4      |")
    print(" --------------------------------------- ")
    print("Digite sua escolha:")

def close_system():
    clean_screen()
    print(" --------------------------------------- ")
    print("|           SISTEMA DE BACKUP           |")
    print("|---------------------------------------|")
    print("|      Sistema fechado com sucesso!     |")
    print(" --------------------------------------- ")

def recover_file():
    pass

def delete_file():
    pass

def open_send_file(filepath, sock):
    with open(filepath, 'rb') as f:
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                break
            print(f"Sending {len(bytes_read)} bytes")  # Depuração
            sock.sendall(bytes_read)
    sock.sendall(b'EOF')
    print("Sent EOF")

def select_file():
    directory = './files'
    files = os.listdir(directory)
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    choice = int(input("Select a file to backup: ")) - 1
    return os.path.join(directory, files[choice]), files[choice]

def init_socket_connection():
    manager_address = ('localhost', 9000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(manager_address)

    filepath, filename = select_file()
    print(f"Selected file: {filename}")
    sock.sendall(os.path.basename(filename).encode('utf-8'))
    
    response = sock.recv(1024).decode('utf-8')
    print(f"Manager response: {response}")
    if response == 'READY':
        open_send_file(filepath, sock)
    
    response = sock.recv(1024).decode('utf-8')
    print(f"Manager response: {response}")
    time.sleep(3)
    
    sock.close()

def main():
    client_choice = 0
    while client_choice != 4:
        client_menu()
        client_choice = int(input())
        if client_choice == 1:
            init_socket_connection()
        elif client_choice == 2:
            print("Implementar ainda")
            time.sleep(3)
        elif client_choice == 3:
            print("Implementar ainda")
            time.sleep(3)
        elif client_choice == 4:
            close_system()
        else:
            clean_screen()
            print(f"O comando {client_choice} é inválido!")
            print("Voltando para tela inicial em 5s...")
            time.sleep(5)

if __name__ == '__main__':
    main()
