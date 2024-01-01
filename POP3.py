import os

def filters_email(directory):
    # Xác định các quy tắc lọc và thư mục tương ứng
    filter_rules = {
        'Inbox': [''],
        'Project': ['ahihi@testing.com', 'ahuu@testing.com'],
        'Important': ['urgent', 'ASAP'],
        'Work': ['report', 'meeting'],
        'Spam': ['virus', 'hack', 'crack']
    }

    # Tạo các thư mục lưu trữ kết quả lọc nếu chưa tồn tại
    for folder in filter_rules.keys():
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Lặp qua từng tệp tin email trong thư mục
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)

            # Đọc nội dung của tệp tin email
            with open(file_path, 'rb') as f:
                email_content = f.read().decode('utf-8', errors='ignore')

            # Áp dụng các quy tắc lọc
            for folder, keywords in filter_rules.items():
                for keyword in keywords:
                    # Kiểm tra từ khóa trong nội dung email
                    if keyword in email_content:
                        # Di chuyển tệp tin email vào thư mục tương ứng
                        new_file_path = os.path.join(directory, folder, filename)
                        os.rename(file_path, new_file_path)
                        print(f'Moved {filename} to {folder} folder')
                        break  # Chỉ di chuyển vào một thư mục duy nhất
    for filename in os.listdir(directory):
        if filename.endswith('.msg'):
            file_path = os.path.join(directory, filename)

            if not os.path.exists(file_path):
                print(f"File {file_path} does not exist. Skipping...")
                continue                   
filters_email('/home/vudeptrai/Documents/vu/Mail_from_Mail_Box')
