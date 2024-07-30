from socket import *

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
                     
sentence = input("Digite algo em letras minúsculas: ")

sen = sentence.encode()
clientSocket.send(sen)
modifiedSentence = clientSocket.recv(1024)
print(f"From server: {modifiedSentence.decode()}")
clientSocket.close()