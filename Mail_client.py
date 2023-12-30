import os
import threading
import time
import json
import socket
import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate

def get_file_size(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)



def create_email(sender_email, recipient_email, cc_email,cc_email_list, bcc_email ,subject, body, attachments=None):
    # Tạo một thông điệp email
    message = MIMEMultipart()
    message['Date'] = formatdate(localtime=True)
    message['From'] = sender_email
    message['To'] = recipient_email
    if cc_email:
        message['Cc'] = ', '.join(cc_email_list) 
    else:
        message['Cc'] = None
    if bcc_email:
        message['Bcc'] = "undisclosed-recupients;"
    else:
        message['Bcc'] = None
        
    message['Subject'] = subject
     
 
    # Thêm nội dung email (plain text)
    message.attach(MIMEText(body, 'plain'))

    
    # Đính kèm file vào email nếu có
    if attachments:
        total_size = 0
        for file_path in attachments:
            try:
                file_size = get_file_size(file_path)
                total_size += file_size
                if total_size > 3:
                    print("Tổng dung lượng file vượt quá 3MB!")
                    break
                with open(file_path, 'rb') as file:
                    attachment = MIMEBase('application', 'octet-stream')
                    attachment.set_payload(file.read())
                    encoders.encode_base64(attachment)
                    attachment.add_header('Content-Disposition', f"attachment; filename= {file_path}")
                    message.attach(attachment)
            except FileNotFoundError:
                print(f"File {file_path} not found!")

    # Trả về nội dung email đã tạo
    return message.as_string()



def send_email(sender_email, smtp_server, smtp_port):
    
    recipient_email = input("TO: ")
    cc_email = input("CC: ")
    cc_email_list = cc_email.split(',')
    cc_email_list = [email.strip() for email in cc_email_list]
    
    bcc_email = input("BCC: ")
    bcc_email_list = bcc_email.split(',')
    bcc_email_list = [email.strip() for email in bcc_email_list]
      
    

    # Tạo kết nối với máy chủ SMTP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((smtp_server, smtp_port))

    # Nhận và in phản hồi từ máy chủ SMTP
    response = client.recv(1024)

    # Gửi lệnh EHLO để bắt đầu phiên làm việc
    client.send(b'EHLO example.com\r\n')
    response = client.recv(1024)

    # Gửi lệnh MAIL FROM để chỉ định người gửi
    client.send(f'MAIL FROM: <{sender_email}>\r\n'.encode('utf-8'))
    response = client.recv(1024)

    # Gửi lệnh RCPT TO để chỉ định người nhận, CC và BCC
    client.send(f'RCPT TO: <{recipient_email}>\r\n'.encode('utf-8'))
    response = client.recv(1024)
    #gửi cc
    if cc_email:
        for cc_email in cc_email_list:
            client.send(f'RCPT TO: <{cc_email}>\r\n'.encode('utf-8'))
            response = client.recv(1024)
    if bcc_email:
        for bcc_email in bcc_email_list:
            client.send(f'RCPT TO: <{bcc_email}>\r\n'.encode('utf-8'))
            response = client.recv(1024)
    # Gửi lệnh DATA để bắt đầu viết nội dung email
    client.send(b'DATA\r\n')
    response = client.recv(1024)


    subject = input("Subject: ")
    body = input("Content: ")
    attach_file = input("Có gửi kèm file (1. có, 2. không): ")
    if attach_file == '1':
        num_files = int(input("Số lượng file muốn gửi: "))
        attachments = []
        for i in range(num_files):
            file_path = input(f"Cho biết đường dẫn file thứ {i + 1}: ")
            attachments.append(file_path)
    elif attach_file == '2':
        attachments = None

    email_content = create_email(sender_email, recipient_email, cc_email,cc_email_list,bcc_email, subject, body, attachments)

    # Gửi nội dung email
    client.sendall(email_content.encode('utf-8'))

    # Kết thúc nội dung email bằng dấu chấm
    client.send("\r\n.\r\n".encode('utf-8'))

    # Nhận và kiểm tra phản hồi từ máy chủ
    response = client.recv(1024).decode('utf-8')
    if "250" in response:
        # Nếu máy chủ phản hồi với mã 250, gửi lệnh QUIT
        client.send("QUIT\r\n".encode('utf-8'))
    else:
        # Nếu không, in ra lỗi và không gửi lệnh QUIT
        print("Error: Failed to send email")
    
    # Nhận phản hồi từ máy chủ SMTP và đóng kết nối
    response = client.recv(1024)
    print(f"Received: {response.decode('utf-8')}")
    client.close()

    print("Connection to SMTP server closed")

def fetch_emails():
    email_server = '127.0.0.1'
    email_port = 3335  # Sử dụng cổng 110 cho giao thức POP3 không qua SSL/TLS

    # Kết nối đến server email
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((email_server, email_port))
    response = sock.recv(1024).decode()
    #print(response)

    # Xác thực với server email
    username = 'vuco@gmail.com'
    password = '123'

    sock.sendall(f'USER {username}\r\n'.encode())
    response = sock.recv(1024).decode()
    # print(response)

    sock.sendall(f'PASS {password}\r\n'.encode())
    response = sock.recv(1024).decode()
    # print(response)
    
    # Lấy số lượng email trong hộp thư đến
    num_emails = 0
    
    sock.sendall('STAT\r\n'.encode())
    response = sock.recv(1024).decode()
    # print(response)
    num_emails = int(response.split()[1])

    # Lấy danh sách các email trong hộp thư đến
    sock.sendall('LIST\r\n'.encode())
    response = sock.recv(1024).decode()
    # print(response)

    
   # Sau khi lấy danh sách các email trong hộp thư đến
    email_ids = response.split()[1:]
    filtered_ids = [email_ids[i] for i in range((len(email_ids))) if i % 2 == 0]
    
    save_directory = '/home/vudeptrai/Documents/vu/Mail_from_Mail_Box'  # Thay đổi đường dẫn này thành đường dẫn thư mục bạn muốn lưu email
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
        file_path = os.path.join(save_directory, f'email_{email_id}.msg')
        with open(file_path, 'wb') as f:
            f.write(email_content)
        print(f'Saved email {email_id} to {file_path}')
        
    # Đóng kết nối
    sock.sendall('QUIT\r\n'.encode())
    response = sock.recv(1024).decode()
    # print(response)




def read_config_json(filename):
    with open(filename, "r") as f:
        config = json.load(f)
    return config








    

def main():
    config = read_config_json('/home/vudeptrai/Documents/vu/config/config.json')
    sender_email = (config["General"]["Username"])
    smtp_server = (config["General"]["MailServer"])
    smtp_port = (config["General"]["SMTP"])
    pop3_port = (config["General"]["POP3"])
    autoload = (config["General"]["Autoload"])
    

    while True:
        print("Chọn chức năng:")
        print("1. Gửi email")
        print("2. Xem danh sách các mail đã nhận")
        print("3. Thoát")

        choice = input("Nhập lựa chọn của bạn : ")
        if choice == "1":
            send_email(sender_email, smtp_server, smtp_port)
        elif choice == "2":
            fetch_emails()
        elif choice == "3":
            print("Đã thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

main()