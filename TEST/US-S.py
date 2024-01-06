import socket
import email

username= "22120437@mmt.edu.vn"
password= "123456"
email_server = '127.0.0.1'
email_port = 3335


sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((email_server, email_port))
response=sock.recv(1024).decode()

sock.sendall(f'USER {username}\r\n'.encode())
response = sock.recv(1024).decode()

sock.sendall(f'PASS {password}\r\n'.encode())
response = sock.recv(1024).decode()

# Lấy số lượng email trong hộp thư đến
sock.sendall('STAT\r\n'.encode())
response = sock.recv(1024).decode()
num_emails = int(response.split()[1])

sock.sendall('LIST\r\n'.encode())
response = sock.recv(1024).decode()

email_ids = response.split()[1:]
print(email_ids)
filtered_ids = [email_ids[i] for i in range((len(email_ids))) if i % 2 == 0]
print(filtered_ids)

# Lặp qua từng email và lấy nội dung
i = 0
for email_id in filtered_ids:# Giả sử filtered_ids chứa các số thứ tự của email như bạn đã lấy được từ danh sách email_ids
    if i < num_emails:
        i += 1
    else:
        break
    sock.sendall(f'RETR {email_id}\r\n'.encode())
    email_content = b''
    while True:
            response = sock.recv(1024)
            email_content += response
            if response.endswith(b'\r\n.\r\n'):
                break


# Đóng kết nối với server email
sock.sendall('QUIT\r\n'.encode())
sock.close()