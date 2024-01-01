match = re.search(r"\+OK\s+(\d+)", response)
if match:
    email_count = int(match.group(1))
else:
    email_count = 0

# Chọn email mới nhất
latest_email_index = email_count

server.send("RETR 71\r\n".encode())
response=server.recv(1024).decode()
print(response)

email_msg = email.message_from_string(response)
if email_msg.is_multipart():
    for part in email_msg.get_payload():
        if part.get_content_type() == 'application/octet-stream':
            # Lưu file xuống thư mục cụ thể
            filename = part.get_filename()
            save_path = os.path.join(save_directory, filename)
            file_data = part.get_payload(decode=True)
            with open(save_path, 'wb') as file:
                file.write(file_data)
            print(f"Tập tin {filename} đã được lưu vào {save_path}.")




###################################################################
            

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

########################################
    
email_count = 1
while True:
    server.sendall('LIST {}\r\n'.format(email_count).encode())
    response = server.recv(1024).decode()
    print(response)
    if response.startswith('+OK'):
        email_count+=1
    else :
        break



######################################
    
while True:
    if response.startswith('+OK'):
        email_count+=1
    else :
        break
    server.sendall('LIST {}\r\n'.format(email_count).encode())
    response = server.recv(1024).decode()
    print(response)
    

print(email_count)