import os
import threading
import time
import json
import socket
import base64
import shutil
import email
import fpdf

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

def fetch_emails(email_server,email_port, username, password):

    # Kết nối đến server email
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((email_server, email_port))
    response = sock.recv(1024).decode()

    # Xác thực với server email
    
    sock.sendall(f'USER {username}\r\n'.encode())
    response = sock.recv(1024).decode()

    sock.sendall(f'PASS {password}\r\n'.encode())
    response = sock.recv(1024).decode()
    
    # Lấy số lượng email trong hộp thư đến
    num_emails = 0
    
    sock.sendall('STAT\r\n'.encode())
    response = sock.recv(1024).decode()
    num_emails = int(response.split()[1])

    # Lấy danh sách các email trong hộp thư đến
    sock.sendall('LIST\r\n'.encode())
    response = sock.recv(1024).decode()

    
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
        file_path = os.path.join(save_directory, f'email_{email_id}.txt') 
        with open(file_path, 'wb') as f:
            f.write(email_content)
        
    # Đóng kết nối
    sock.sendall('QUIT\r\n'.encode())
    response = sock.recv(1024).decode()

filter_rules = {
    'Inbox': ['Others'],  # Thư mục mặc định cho các email không phù hợp với bất kỳ quy tắc nào
    'Project': ['ahihi@testing.com', 'ahuu@testing.com'],
    'Important': ['urgent', 'ASAP'],
    'Work': ['report', 'meeting'],
    'Spam': ['virus', 'hack', 'crack']
}


def filters_email(directory):
    save_directory = '/home/vudeptrai/Documents/vu/Mail_from_Mail_Box'  
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Duyệt qua tất cả các email đã tải trong đường dẫn thư mục save_directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)

            # Đọc nội dung email từ file
            with open(file_path, 'rb') as f:
                email_content = f.read().decode(errors='ignore')

            # Biến lưu trữ tên thư mục, mặc định là Inbox
            matched_rule = 'Inbox'  
            for folder, keywords in filter_rules.items():
                for keyword in keywords:
                    if keyword.lower() in email_content.lower():
                        matched_rule = folder
                        break
                if matched_rule != 'Inbox':
                    break

            new_folder = os.path.join(save_directory, matched_rule)
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)

            new_file_path = os.path.join(new_folder, filename)
            shutil.move(file_path, new_file_path)

def retrieve_email_sender(sender,e_content):
    # Lấy sendername từ email

    # Kiểm tra xe email có đính kèm file hay không
    index = e_content.find("------------") 
    if index == -1 : 
        
        # Nếu không đính kèm file
        lines = e_content.split("\n")
        sender_line = lines[7]
        start_index = sender_line.index("<")
        end_index = sender_line.index(">")
        sender = sender_line[start_index + 1:end_index]
    else :

        # Nếu có đính kèm file
        end_index = e_content.find("--------------")
        Content = e_content[:end_index]
        lines = Content.split("\n")
        sender_line = lines[8]
        start_index = sender_line.index("<")
        end_index = sender_line.index(">")
        sender = sender_line[start_index + 1:end_index] 

    # Trả về sendername
    return sender

def retrieve_email_subject(subject,e_content):
    #Lấy subject từ email

    # Kiểm tra xe email có đính kèm file hay không
    index = e_content.find("------------")
    if index == -1 : 

        # Nếu không đính kèm file
        lines = e_content.split("\n")
        subject_line = lines[8]
        subject = subject_line.split(":")[1].strip()
    else :

        # Nếu có đính kèm file
        end_index = e_content.find("--------------")
        Content = e_content[:end_index]
        lines = Content.split("\n")
        subject_line = lines[9]
        subject = subject_line.split(":")[1].strip()

    # Trả về subject
    return subject

def retrieve_email_body(body,email_content) :
    #Lấy nội dung từ email

    # Kiểm tra xe email có đính kèm file hay không
    index = email_content.find("------------")
    if index == -1:

        # Nếu không đính kèm file
        start_index = email_content.find("\n\n") + 2
        end_index = email_content.find("\n\n", start_index)
        body = email_content[start_index:end_index]
    else:

        # Nếu có đính kèm file
        end_index = email_content.find("--------------")
        Content = email_content[:end_index]
        email_content = email_content.replace(Content,"")
        start_index = email_content.find("--------------")
        end_index = email_content.find("--------------",start_index+1)
        Body = email_content[start_index:end_index]
        lines = Body.split('\n')
        body_content = '\n'.join(lines[4:])
        body=body_content.rstrip()

    # Trả về nội dung thân thư 
    return body

def retrieve_email_file(email_content):
    #Hàm kiểm tra xem email có đính kèm file không
     
    index = email_content.find("------------")
    if index == -1 :

        # Nếu không đính kèm file
        print("Không có file đính kèm.")
    else:
        # Nếu có đính kèm file

        #Biến email_content lưu trữ toàn bộ nội dung email, ta sẽ lần lượt xóa các phần nội dung không cần thiết, chỉ để lại phần nội dung chứa tên và nội dung file
        #Xóa Header
        end_index = email_content.find("--------------")
        Content = email_content[:end_index]
        email_content = email_content.replace(Content,"")

        #Xóa Body
        start_index = email_content.find("--------------")
        end_index = email_content.find("--------------",start_index+1)
        Body = email_content[start_index:end_index]
        email_content = email_content.replace(Body, "")

        #File
        f_name_array = [] # Danh sách lưu trữ tên file
        f_name_count = 0
        f_content_array = [] # Danh sách lưu trữ nội dung file
        f_content_count = 0
        start_index = email_content.find("--------------")
        while True:
            end_index = email_content.find("--------------",start_index+1)
            if end_index == -1 : break
            file_part = email_content[start_index:end_index]

            # file_name lưu vào file_name_array
            name_start_index = file_part.find('name="') + len('name="')
            name_end_index = file_part.find('"', name_start_index )
            file_name = file_part[name_start_index:name_end_index]
            datatybe_name = file_name.find("?UTF-8?B?")
            if datatybe_name == -1:
                f_name_array.append(file_name)
                f_name_count = f_name_count + 1
            else:
                encoded_data = file_name.split("?B?")
                encoded_data=str(encoded_data)
                decoded_data = base64.b64decode(encoded_data)
                file_name = decoded_data.decode('utf-8')
                file_name= file_name.replace("Q1|", "")
                f_name_array.append(file_name)
                f_name_count = f_name_count + 1
            
            # file_content lưu vào file_content_array
            sections = file_part.split('\n\n')
            file_content = sections[1]
            f_content_array.append(file_content)
            f_content_count + 1
            email_content=email_content.replace(file_part, "")
        while f_name_count >0 :
            print("Tên file: ",f_name_array[f_name_count-1])
            f_name_count = f_name_count- 1
            f_content_count = f_content_count - 1

        

def select_email(directory, email_seen_status):
    # Hàm thực hiện chọn thư mục và email 

    print("Đây là danh sách các folder trong mailbox của bạn:")
    all_folder = next(os.walk(directory))[1]
    i=1
    for folder in all_folder :
        print(i,'.',folder)
        i=i+1
    ans = input("Bạn muốn xem foler nào(Nhấn enter để thoát ra ngoài): ")
    if ans == "": 
        print("\n")
        return
    select_folder_index = int(ans) - 1
    if select_folder_index<len(all_folder):
        select_folder = all_folder[select_folder_index]
        select_folder_path = os.path.join(directory,select_folder)
        all_sonfolder_email = os.listdir(select_folder_path)
        while True:
            i=1
            print("Đây là danh sách trong",select_folder,"folder")
            for file in all_sonfolder_email:
                email_path = os.path.join(select_folder_path,file)
                with open(email_path,'r') as e:
                    e_content = e.read()
                sender = ""
                subject = ""
                sender = retrieve_email_sender(sender,e_content)
                subject = retrieve_email_subject(subject,e_content)
                if file in email_seen_status:
                    print(i,'.',sender,',',subject)
                else:
                    print(i,'.',"<chưa đọc>",sender,',',subject)
                i=i+1
            while True:
                ans = input("Bạn muốn đọc Email thứ mấy(hoặc nhấn enter để thoát ra ngoài, hoặc nhấn 0 để xem lại danh sách email): ")
                if ans == "0": break
                elif ans == "": return
                else:
                    selected_email_index = int(ans) -1
                    if selected_email_index<len(all_sonfolder_email):
                        selected_email = all_sonfolder_email[selected_email_index]
                        email_seen_status.append(selected_email)
                        selected_email_path = os.path.join(select_folder_path,selected_email)
                        print("Nội dung email của email thứ",selected_email_index + 1,":")
                        with open(selected_email_path,'r') as e:
                            email_content = e.read()
                        body=""
                        body = retrieve_email_body(body,email_content)
                        print(body)
                        retrieve_email_file(email_content)


def auto_download(email_server,email_port, username, password,autoload,directory,stop_thread):
    # Hàm thực hiện tải email tự động theo thời gian file config
    while not stop_thread.is_set():
        fetch_emails(email_server,email_port, username, password)
        filters_email(directory)
        time.sleep(autoload)

def read_config_json(filename):
    # Hàm đọc file config
    with open(filename, "r") as f:
        config = json.load(f)
    return config
    
def main():
    config = read_config_json('/home/vudeptrai/Documents/vu/config/config.json')
    sender_email = (config["General"]["Username"])
    password = (config["General"]["Password"])
    smtp_server = (config["General"]["MailServer"])
    smtp_port = (config["General"]["SMTP"])
    email_server = (config["General"]["MailServer"])
    email_port = (config["General"]["POP3"])
    autoload = (config["General"]["Autoload"])
    

    filter_rules = {
    'Inbox': ['Others'],  # Thư mục mặc định cho các email không phù hợp với bất kỳ quy tắc nào
    'Project': ['ahihi@testing.com', 'ahuu@testing.com'],
    'Important': ['urgent', 'ASAP'],
    'Work': ['report', 'meeting'],
    'Spam': ['virus', 'hack', 'crack']
}
    
    email_seen_status = [] # Danh sách quản lý những email đã đọc
    fetch_emails(email_server,email_port, sender_email, password)
    filters_email('/home/vudeptrai/Documents/vu/Mail_from_Mail_Box')

    # Thực hiện tự động tải email về theo thời gian file config
    directory = '/home/vudeptrai/Documents/vu/Mail_from_Mail_Box'
    stop_thread = threading.Event()
    autodown_email = threading.Thread(target=auto_download,args=(email_server, email_port, sender_email, password, autoload, directory,stop_thread))
    autodown_email.start()

    while True:
        print("Chọn chức năng:")
        print("1. Gửi email")
        print("2. Xem danh sách các mail đã nhận")
        print("3. Thoát")

        choice = input("Nhập lựa chọn của bạn : ")
        if choice == "1":
            send_email(sender_email, smtp_server, smtp_port)
        elif choice == "2":
            select_email('/home/vudeptrai/Documents/vu/Mail_from_Mail_Box',email_seen_status)
        elif choice == "3":
            stop_thread.set()
            autodown_email.join()
            # Thực hiện dừng tự động tải email khi kết thúc chương trình. Hoạt động dừng lại này cần một ít thời gian
            
            print("Đã thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
    

main()