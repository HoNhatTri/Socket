import socket
import os
import base64



# def fetch_emails():
#     email_server = '127.0.0.1'
#     email_port = 3335  # Sử dụng cổng 110 cho giao thức POP3 không qua SSL/TLS

#     # Kết nối đến server email
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect((email_server, email_port))
#     response = sock.recv(1024).decode()
#     #print(response)

#     # Xác thực với server email
#     username = 'vuco@gmail.com'
#     password = '123'

#     sock.sendall(f'USER {username}\r\n'.encode())
#     response = sock.recv(1024).decode()
#     # print(response)

#     sock.sendall(f'PASS {password}\r\n'.encode())
#     response = sock.recv(1024).decode()
#     # print(response)
    
#     # Lấy số lượng email trong hộp thư đến
#     num_emails = 0
    
#     sock.sendall('STAT\r\n'.encode())
#     response = sock.recv(1024).decode()
#     # print(response)
#     num_emails = int(response.split()[1])

#     # Lấy danh sách các email trong hộp thư đến
#     sock.sendall('LIST\r\n'.encode())
#     response = sock.recv(1024).decode()
#     # print(response)

    
#    # Sau khi lấy danh sách các email trong hộp thư đến
#     email_ids = response.split()[1:]
#     filtered_ids = [email_ids[i] for i in range((len(email_ids))) if i % 2 == 0]
    
#     save_directory = '/home/vudeptrai/Documents/vu/Mail_from_Mail_Box'  # Thay đổi đường dẫn này thành đường dẫn thư mục bạn muốn lưu email
#     if not os.path.exists(save_directory):
#         os.makedirs(save_directory)

#         # Lặp qua từng ID và lấy nội dung email
#     i = 0
#     for email_id in filtered_ids:# Giả sử filtered_ids chứa các số thứ tự của email như bạn đã lấy được từ danh sách email_ids
#         if i < num_emails:
#             i += 1
#         else:
#             break
#         sock.sendall(f'RETR {email_id}\r\n'.encode())
#         email_content = b''
#         while True:
#             response = sock.recv(1024)
#             email_content += response
#             if response.endswith(b'\r\n.\r\n'):
#                 break
#         # Lưu trữ email vào thư mục đã chỉ định
#         file_path = os.path.join(save_directory, f'email_{email_id}.txt')
#         with open(file_path, 'wb') as f:
#             f.write(email_content)
#         print(f'{email_id} Đã lưu vào thư mục')
        
#     # Đóng kết nối
#     sock.sendall('QUIT\r\n'.encode())
#     response = sock.recv(1024).decode()
#     # print(response)
    
# fetch_emails()

def decode_base64_file(input_file, output_file):
    with open(input_file, 'r') as file:
        encoded_data = file.read()

    decoded_data = base64.b64decode(encoded_data)

    with open(output_file, 'wb') as file:
        file.write(decoded_data)

def display_email_content(eml_file):
    with open(eml_file, 'r') as file:
        lines = file.readlines()

    email_content = ""
    attachment_data = ""
    is_attachment = False

    for line in lines:
        if line.startswith('Subject:'):
            print("Subject:", line[8:].strip())
        elif line.startswith('From:'):
            print("From:", line[5:].strip())
        elif line.startswith('To:'):
            print("To:", line[3:].strip())
        elif line.startswith('Date:'):
            print("Date:", line[5:].strip())
        elif line.startswith('Content-Type:'):
            content_type = line[13:].strip()
            if 'multipart' in content_type:
                is_attachment = True
        elif line.startswith('Content-Disposition:'):
            attachment_info = line[20:].strip()
            print(f"Attachment Info: {attachment_info}")
        elif line.startswith('Content-Transfer-Encoding: base64'):
            is_attachment = True
        elif line.startswith('------') and is_attachment:
            is_attachment = False
            attachment_data += line
        elif is_attachment:
            attachment_data += line

        else:
            email_content += line

    print("\nEmail Content:")
    print(email_content)

    if attachment_data:
        attachment_file = eml_file.replace('.txt', '_attachment.txt')
        with open(attachment_file, 'w') as file:
            file.write(attachment_data)

        print(f"\nAttachment saved as: {attachment_file}")

def decode_email_attachments(directory):
    if not os.path.exists(directory):
        print(f"Thư mục '{directory}' không tồn tại.")
        return

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.txt'):
            display_email_content(file_path)

decode_email_attachments('/home/vudeptrai/Documents/vu/Mail_from_Mail_Box')