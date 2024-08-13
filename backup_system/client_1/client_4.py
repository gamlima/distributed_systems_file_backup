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
    print("Recuperar arquivo ainda não implementado.")
    time.sleep(3)

def delete_file():
    print("Excluir arquivo ainda não implementado.")
    time.sleep(3)

def open_send_file(filepath, sock):
    try:
        with open(filepath, 'rb') as f:
            while True:
                bytes_read = f.read(1024)  # Lê o arquivo em blocos de 1024 bytes
                if not bytes_read:
                    break
                print(f"Sending {len(bytes_read)} bytes")  # Depuração
                sock.sendall(bytes_read)
        sock.sendall(b'EOF')  # Sinaliza o fim do arquivo
        print("Sent EOF")
    except Exception as e:
        print(f"An error occurred while sending the file: {e}")

def select_file():
    directory = './files'
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return None, None
    files = os.listdir(directory)
    if not files:
        print(f"No files found in {directory}.")
        return None, None
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    choice = int(input("Select a file to backup: ")) - 1
    if choice < 0 or choice >= len(files):
        print("Invalid file choice.")
        return None, None
    return os.path.join(directory, files[choice]), files[choice]

def init_socket_connection():
    try:
        # Conecta ao gerenciador
        manager_address = ('localhost', 9000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(manager_address)
        sock.sendall(b'SERVER ADDRESS')
        server_address = sock.recv(1024).decode('utf-8')
        server_ip, server_port = server_address.split(':')
        server_port = int(server_port)
        sock.close()

        # Conecta ao servidor escolhido
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        sock.sendall(b'BACKUP')
        response = sock.recv(1024).decode('utf-8')

        if response == 'READY':
            filepath, filename = select_file()
            if filepath:
                print(f"Selected file: {filename}")
                sock.sendall(filename.encode('utf-8'))
                response = sock.recv(1024).decode('utf-8')
                print(f"Server response: {response}")
                if response == 'READY FOR RECEIVE':
                    open_send_file(filepath, sock)
                    response = sock.recv(1024).decode('utf-8')
                    print(f"Server response: {response}")
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
                recover_file()
            elif client_choice == 3:
                delete_file()
            elif client_choice == 4:
                close_system()
            else:
                clean_screen()
                print(f"O comando {client_choice} é inválido!")
                print("Voltando para tela inicial em 5s...")
                time.sleep(5)
        except ValueError:
            clean_screen()
            print("Entrada inválida. Por favor, digite um número.")
            time.sleep(3)

if __name__ == '__main__':
    main()
