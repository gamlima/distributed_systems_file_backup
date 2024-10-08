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
    
    # Enviar uma mensagem de finalização mais robusta
    sock.sendall(b'EOF')
    print("Sent EOF")
    
    # Esperar confirmação do servidor
    response = sock.recv(1024).decode('utf-8')
    if response == 'RECEIVED':
        print("Server confirmed receipt of file.")
    else:
        print("Server did not confirm file receipt.")

def select_file():
    directory = './files'
    files = os.listdir(directory)
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    choice = int(input("Select a file to backup: ")) - 1
    if choice < 0 or choice >= len(files):
        print("Invalid choice.")
        return None, None
    return os.path.join(directory, files[choice]), files[choice]

def init_socket_connection():
    try:
        manager_address = ('localhost', 9000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(manager_address)

        sock.sendall('SERVER ADDRESS 3'.encode('utf-8'))
        server_address = sock.recv(1024).decode('utf-8')
        server_ip, server_port = server_address.split(':')
        server_port = int(server_port)
        sock.close()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        sock.sendall('BACKUP 3'.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')

        if response == 'READY':
            filepath, filename = select_file()
            if filepath:
                print(f"Selected file: {filename}")
                sock.sendall(os.path.basename(filename).encode('utf-8'))
                response = sock.recv(1024).decode('utf-8')
                print(f"Server response: {response}")
                if response == 'READY FOR RECEIVE':
                    open_send_file(filepath, sock)
                else:
                    print("Server is not ready to receive the file.")
        else:
            print("Server not ready.")

        sock.close()
        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    client_choice = 0
    while client_choice != 4:
        client_menu()
        try:
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
        except ValueError:
            print("Escolha inválida. Tente novamente.")
            time.sleep(3)

if __name__ == '__main__':
    main()
