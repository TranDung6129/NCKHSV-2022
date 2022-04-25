import os
import pandas as pd
import numpy as np

'''Em chưa nghĩ ra cách để chỉ chạy mà không cần làm gì cả, thế nên trước mắt thì sẽ giải quyết 
bằng cách là để người sử dụng về sau tự nhập thông tin cột, em sẽ nghĩ cách để tự động hết sau ạ'''
filepath = input("Xin mời nhập đường dẫn tới file: ")
basename = os.path.basename(filepath)
print(basename)

classroom = pd.read_excel(filepath, sheet_name = 'BIỂU ĐỒ (S)')
# Tên của cột Số phòng mới và Số chỗ
print(f"Dưới đây là danh sách tên cột của phòng, hãy tìm tên của cột chứa danh sách phòng học và tên của cột ghi sức "
      f"chứa của phòng và ghi vào bên dưới \n \n {classroom.columns} ") 
classroom_column = input("Tên cột chứa danh sách phòng học là: ")
classroom_capacity = input("Tên của cột chứa sức chứa của các phòng học là: ")


# Xử lý và làm sạch dữ liệu

classroom = classroom[[classroom_column, classroom_capacity]]
# Xóa tất cả các hàng chứa toàn bộ dữ liệu trống
classroom.dropna(axis = 0, how = 'all')
# Đổi tên cột để phù hợp với mô tả của mô
classroom.rename(columns = {classroom_column: 'Tên phòng', classroom_capacity: 'Sức chứa'}, inplace = True)
# Xóa hai cột trống phía trên (đoạn này cần kiểm tra)
classroom.drop(labels = [0, 1], inplace = True)
# Đoạn này cũng cần kiểm tra lại, xóa lần nữa cho chắc
class_room = classroom.dropna(axis = 0, how = 'all')
# Reset lại index của bảng
class_room = class_room.reset_index(drop = True)


# In ra danh sách
print(f"Dưới đây là danh sách phòng học và sức chứa của phòng: \n\n {class_room}")

