import base64
from reportlab.pdfgen import canvas
import os

# Đường dẫn đến thư mục lưu trữ tệp tin PDF
output_folder = "/Work_File"

# Nội dung file cần mã hóa và ghi vào tệp tin PDF
file_content = "Xin chào, tôi tên là Trí"

# Mã hóa nội dung file thành chuỗi base64
encoded_data = base64.b64encode(file_content.encode("utf-8"))
print(encoded_data)


# Giải mã chuỗi base64
decoded_data = base64.b64decode(encoded_data)

# Chuyển đổi dữ liệu giải mã thành chuỗi
decoded_content = decoded_data.decode("utf-8",errors='ignore')

# Tạo đường dẫn và tên tệp tin PDF
pdf_path = os.path.join(output_folder, "file.pdf")

# Tạo một đối tượng canvas PDF và ghi nội dung vào tệp tin PDF
pdf = canvas.Canvas(pdf_path)
pdf.drawString(50, 800, decoded_content)
pdf.save()

print("Tệp tin PDF đã được tạo và lưu thành công vào thư mục:", output_folder)