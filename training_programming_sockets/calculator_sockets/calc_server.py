from socket import *

def calculator(sentence):
    decoded_sentence = sentence.decode('utf-8')

    op, num1, num2 = decoded_sentence.split()
    print(f"{op}, {num1}, {num2}")
    if op == "SOMA":
        result = str(float(num1)+float(num2))
    elif op == "SUB":
        result = str(float(num1)-float(num2))
    elif op == "MULT":
        result = str(float(num1)*(float(num2)))
    elif op == "DIV":
        if(num2 == "0"):
            result = "Error. Division by zero!"
        else:
            result = str(float(num1)/float(num2))
    else:
        result = "Error. Unknown operation!"
    return result

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))

serverSocket.listen(1)

print("The server is ready to receive")

while(1):
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    print("Request received!")
    result = (calculator(sentence)).encode()
    connectionSocket.send(result)
    connectionSocket.close()