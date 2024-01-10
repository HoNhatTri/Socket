
import os

def AA(path_file):
    with open(path_file,'a') as w:
        w.write("\nsos")
# Đường dẫn đến thư mục lưu trữ tệp tin PDF
output_folder = "/Work_File"
file_name = "text1.txt"

# Nội dung file cần mã hóa và ghi vào tệp tin PDF
file_content = "Xin chào, tôi tên là Trí"
path_file = os.path.join(output_folder,file_name)
with open(path_file,'w') as p:
    p.write(file_content)
with open(path_file,'a') as p:
    p.write("\n<seen>")
AA(path_file)
