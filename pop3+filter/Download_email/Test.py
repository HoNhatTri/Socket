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

server.send(b'STAT\r\n')
response=server.recv(1024).decode()
print(response)

email_count = 1
email_received = 0

while email_received < 20:
    server.sendall('UIDL {}\r\n'.format(email_count).encode())
    response = server.recv(1024).decode()
    print(response)
    
    server.sendall('TOP {} 1 \r\n'.format(email_count).encode())
    response = server.recv(1024).decode()
    print(response)
    
    email_count += 1
    email_received += 1 if response.startswith('+OK') else 0

    if email_count > 100:
        # Đảm bảo vòng lặp không vô hạn nếu không tìm thấy đủ 20 email
        break


server.sendall(b'QUIT\r\n')
response=server.recv(1024).decode()
print(response)
server.close()