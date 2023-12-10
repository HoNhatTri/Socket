import socket

HOST = '127.0.0.1'
PORT = 9090

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Client connect to server with port: " + str(PORT))
client.connect((HOST,PORT))
try:
    while True:
        message=input("Client : ")
        client.send(message.encode('utf-8'))


        if message == "Quit":
            print("Client close!")
            break


        message_1=client.recv(1024).decode('utf-8')
        print("Server : "+message_1)
finally:
    client.close()