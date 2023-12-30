import socket
import re
import base64
import os
def decode_attachments(host, port, username, password):
    # Tạo kết nối đến server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    response = sock.recv(1024).decode()
    #print(response)
    
    sock.sendall(f'USER {username}\r\n'.encode())
    response = sock.recv(1024).decode()
    # print(response)

    sock.sendall(f'PASS {password}\r\n'.encode())
    response = sock.recv(1024).decode()
    # print(response)

    # Lấy danh sách email
    sock.send(b"LIST\r\n")
    data = sock.recv(1024)
    while data:
        tokens = data.decode("utf-8").split()
        if tokens[0] == "EXISTS":
            msgid = int(tokens[1])

    # Lấy nội dung email
    sock.send(b"RETR {}\r\n".format(msgid))
    data = sock.recv(1024)
    while data:
        email_content += data
        data = sock.recv(1024)

    # Tìm phần đính kèm
    match = re.search(r'Content-Transfer-Encoding: base64\r\nContent-Disposition: *attachment; *filename=(.*)\r\n\r\n([\s\S]*)', email_content)
    if match:
        file_name = match.group(1)
        file_content = match.group(2)

        # Giải mã nội dung attachment
        decoded_content = base64.b64decode(file_content)
        save_directory = '/home/vudeptrai/Documents/vu/Mail_from_Mail_Box'
        # Lưu lại file đã giải mã
        file_path = os.path.join(save_directory, file_name)
        with open(file_path, "wb") as f:
            f.write(decoded_content)

# Ví dụ sử dụng
decode_attachments("127.0.0.1", 3335, "vuco@gmail.com", "123")
