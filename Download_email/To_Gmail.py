import socket
import base64
import ssl

# Thông tin server email
email_server = 'smtp.gmail.com'
email_port = 587 #465 #587

# Kết nối đến server email
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((email_server, email_port))
response = sock.recv(1024).decode()
print(response)

sock.sendall('EHLO mail.google.com\r\n'.encode())
response = sock.recv(1024).decode()
print(response)

sock.sendall('STARTTLS\r\n'.encode())
response = sock.recv(1024).decode()
print(response)
context = ssl.create_default_context()
sock = context.wrap_socket(sock, server_hostname='smtp.gmail.com')
sock.sendall('EHLO example.com\r\n'.encode())
response = sock.recv(1024).decode()
print(response)

username = 'nhattri140904@gmail.com'
password = 'hfgd gque yyvy oiwv'
#password = '0935660166b'

sock.sendall('AUTH LOGIN\r\n'.encode())
response = sock.recv(1024).decode()
print(response)

sock.sendall(base64.b64encode(username.encode()) + b'\r\n')
response = sock.recv(1024).decode()
print(response)

sock.sendall(base64.b64encode(password.encode()) + b'\r\n')
response = sock.recv(1024).decode()
print(response)

sock.sendall('SELECT INBOX\r\n'.encode())
response = sock.recv(1024).decode()
print(response)

# Gửi lệnh để lấy số lượng email trong hộp thư đến
sock.sendall('SEARCH ALL\r\n'.encode())
response = sock.recv(1024).decode()
print(response)

# Lấy danh sách các ID của email trong hộp thư đến
email_ids = response.split()[1:]

# Lặp qua từng ID và lấy nội dung email
for email_id in email_ids:
    sock.sendall(f'FETCH {email_id} BODY[TEXT]\r\n'.encode())
    response = sock.recv(1024).decode()
    print(response)

# Đóng kết nối
sock.sendall('QUIT\r\n'.encode())
sock.close()