import socket

HOST='127.0.0.1'
PORT=9090

sever=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sever.bind((HOST, PORT))
print("Waiting for Client...")
sever.listen(5)
communication_socket,address = sever.accept()
try:
    print("Connect Success!")
    while True:
        message=communication_socket.recv(1024).decode('utf-8')
        if message == "Quit":
            break

        
        if len(message) >0:
            print("Client : "+message)


        message_1=input("Server : ")
        communication_socket.send(message_1.encode('utf-8'))
finally:
    communication_socket.close()