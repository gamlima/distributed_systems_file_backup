from socket import *

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
                     
sentence = input("Digite uma operação no formato especificado (OP Num1 Num2): ")

sen = sentence.encode()
clientSocket.send(sen)
result = clientSocket.recv(1024)
print(f"Result from server: {result.decode()}")
clientSocket.close()