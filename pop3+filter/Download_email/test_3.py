import socket
import ssl
import email
import os
import re


# Thông tin server POP3
pop3_server = 'pop.gmail.com'
pop3_port = 995
username = 'nhattri140904@gmail.com'
password = 'hfgd gque yyvy oiwv'
#password = '0935660166b'
save_directory = 'C:/Work/'

# Kết nối đến server POP3
context = ssl.create_default_context()
server=context.wrap_socket(socket.socket(socket.AF_INET),server_hostname = pop3_server)
server.connect((pop3_server,pop3_port))
response = server.recv(1024).decode()
print(response)

server.sendall(f'USER {username}\r\n'.encode())
response=server.recv(1024).decode()
print(response)

server.sendall(f'PASS {password}\r\n'.encode())
response=server.recv(1024).decode()
print(response)

server.send(b'LIST 15\r\n')
response=server.recv(1024).decode()
print(response)

retr_command = f'RETR 15\r\n'.encode()
server.send(retr_command)
response=server.recv(1024).decode()
print(response)

server.sendall(b'QUIT\r\n')
response=server.recv(1024).decode()
print(response)
server.close()