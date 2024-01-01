import os
import shutil

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

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)

            # Đọc nội dung email từ file
            with open(file_path, 'rb') as f:
                email_content = f.read().decode(errors='ignore')

            # Áp dụng quy tắc lọc và di chuyển email vào thư mục tương ứng
            matched_rule = 'Inbox'  # Mặc định di chuyển vào thư mục 'Inbox' nếu không phù hợp với bất kỳ quy tắc nào
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
            print(f'Moved email {filename} to {new_file_path}')

# Thực hiện phân loại email trong thư mục đã lưu trữ
filters_email('/home/vudeptrai/Documents/vu/Mail_from_Mail_Box')
