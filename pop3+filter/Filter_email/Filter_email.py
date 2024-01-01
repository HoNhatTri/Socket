import os
import shutil

def filters_email(directory):
    # Đường dẫn thư mục lưu trữ các email được phân loại
    save_directory = '/home/vudeptrai/Documents/vu/Mail_from_Mail_Box'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for filename in os.listdir(directory):
        if filename.endswith('.msg'):
            file_path = os.path.join(directory, filename)

            # Đọc nội dung email từ file
            with open(file_path, 'rb') as f:
                email_content = f.read().decode(errors='ignore')

            # Áp dụng quy tắc lọc và di chuyển email vào thư mục tương ứng
            if 'ahihi@testing.com' in email_content or 'ahuu@testing.com' in email_content:
                new_folder = os.path.join(save_directory, 'Project')
            elif 'urgent' in email_content.upper() or 'ASAP' in email_content.upper():
                new_folder = os.path.join(save_directory, 'Important')
            elif 'report' in email_content.lower() or 'meeting' in email_content.lower():
                new_folder = os.path.join(save_directory, 'Work')
            elif 'virus' in email_content.lower() or 'hack' in email_content.lower() or 'crack' in email_content.lower():
                new_folder = os.path.join(save_directory, 'Spam')
            else:
                new_folder = os.path.join(save_directory, 'Others')

            # Kiểm tra và di chuyển email vào thư mục mới
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)

            new_file_path = os.path.join(new_folder, filename)
            shutil.move(file_path, new_file_path)
            print(f'Moved email {filename} to {new_file_path}')

# Thực hiện phân loại email trong thư mục đã lưu trữ
filters_email('/home/vudeptrai/Documents/vu/Mail_from_Mail_Box')
