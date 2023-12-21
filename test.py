import socket

def get_mail():
    host = 'localhost'
    port = 3335
    
    # Kết nối đến server POP3
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except Exception as e:
        print(e)
        return None

    # Kiểm tra kết nối thành công
    if sock.recv(1).decode("utf-8") != b"+OK":
        return None

    # Lấy danh sách mail
    sock.sendall(b"LIST").encode("utf-8")
    resp = sock.recv(1024).decode("utf-8")
    if resp == "-ERR":
        return None

    # Lấy nội dung từng mail
    for line in resp.splitlines():
        # Loại bỏ các dòng trống và dòng bắt đầu bằng dấu #
        if len(line) > 0 and line[0] != "#":
            index, size = line.split()
            sock.sendall(b"RETR " + index.encode("utf-8"))
            resp = sock.recv(size).decode("utf-8")
            # Trả về nội dung mail
            yield resp

    # Xóa mail khỏi server (tùy chọn)
    sock.sendall(b"QUIT").encode("utf-8")
    resp = sock.recv(1024).decode("utf-8")
    if resp == "-ERR":
        return None

# Lấy mail từ server
    for mail in get_mail():
        print(mail)

get_mail()
