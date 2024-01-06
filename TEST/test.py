import socket
import os
import email



username= "22120437@mmt.edu.vn"
password= "123456"
email_server = '127.0.0.1'
email_port = 3335

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((email_server, email_port))
response = sock.recv(1024).decode()
#print(response)

    # Xác thực với server email
    
sock.sendall(f'USER {username}\r\n'.encode())
response = sock.recv(1024).decode()
#print(response)

sock.sendall(f'PASS {password}\r\n'.encode())
response = sock.recv(1024).decode()
    # print(response)
    
    # Lấy số lượng email trong hộp thư đến
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
save_directory_file='C:/Work_File'  
if not os.path.exists(save_directory):
    os.makedirs(save_directory)
if not os.path.exists(save_directory_file):
    os.makedirs(save_directory_file)

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
    file_path = os.path.join(save_directory, f'email_{email_id}.eml') #hoặc txt
    with open(file_path, 'wb') as f:
            f.write(email_content)
    print(f'Saved email {email_id} to {file_path}')

    with open(file_path,'r') as f:
        email_content=f.read()
        email_message = email.message_from_string(email_content)
        for part in email_message.walk():
            content_disposition = part.get("Content-Disposition")  #Nó luôn ra None mặc dù trong email có hiện là attachment
            #print(content_disposition)
            if content_disposition == 'attachment':
                file_name = part.get_filename()
                ans = input("Trong email này có attached file {filename}, bạn có muốn save không:(có/không) ")
                if ans == "có":
                    save_path = os.path.join(save_directory, file_name)
                    with open(save_path, 'wb') as file:
                        file.write(part.get_payload(decode=True))
                    print("Lưu tệp tin {file_name} thành công.")
                if ans == "không" :
                     print("Không lưu tệp tin {file_name}.")
            else:
                print("Không có file đính kèm.")
            
    # Đóng kết nối
sock.sendall('QUIT\r\n'.encode())
response = sock.recv(1024).decode()
#print(response)