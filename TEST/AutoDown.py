import socket
import os
import email
import time

username = "22120437@mmt.edu.vn"
password = "123456"
email_server = '127.0.0.1'
email_port = 3335
time_config = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((email_server, email_port))
response = sock.recv(1024).decode()

# Xác thực với server email

sock.sendall(f'USER {username}\r\n'.encode())
response = sock.recv(1024).decode()

sock.sendall(f'PASS {password}\r\n'.encode())
response = sock.recv(1024).decode()

save_directory = 'C:/Work'
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

num_emails = 0
    
sock.sendall('STAT\r\n'.encode())
response = sock.recv(1024).decode()
#print(response)
num_emails = int(response.split()[1])

    # Lấy danh sách các email trong hộp thư đến
sock.sendall('LIST\r\n'.encode())
response = sock.recv(1024).decode()
#print(response)

    
   # Sau khi lấy danh sách các email trong hộp thư đến
email_ids = response.split()[1:]
filtered_ids = [email_ids[i] for i in range((len(email_ids))) if i % 2 == 0]
    
save_directory = 'C:/Work'
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

        # Lặp qua từng ID và lấy nội dung email
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
        # Lưu trữ email vào thư mục đã chỉ định
    file_path = os.path.join(save_directory, f'email_{email_id}.txt') #hoặc eml
    with open(file_path, 'wb') as f:
            f.write(email_content)
    print(f'Saved email {email_id} to {file_path}')
    if i<num_emails :
        time.sleep(time_config)

sock.sendall('QUIT\r\n'.encode())
response = sock.recv(1024).decode()