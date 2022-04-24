import os
import pandas as pd
import numpy as np


filepath = 'D:/Nghiên cứu ứng dụng/Bài toán lập lịch/TKB-SIE-ky-20212-14.4.22.xlsx'
basename = os.path.basename(filepath)
print(basename)

classroom = pd.read_excel(filepath, sheet_name = 'BIỂU ĐỒ (S)')
# Tên của cột Số phòng mới và Số chỗ
classroom = classroom[['Unnamed: 39', 'Unnamed: 41']]
# Xóa tất cả các hàng chứa toàn bộ dữ liệu trống 
classroom.dropna(axis = 0, how = 'all')
# Đổi tên cột để phù hợp với mô tả của mô 
classroom.rename(columns = {'Unnamed: 39': 'Tên phòng', 'Unnamed: 41': 'Sức chứa'}, inplace = True)
# Xóa hai cột trống phía trên (đoạn này cần kiểm tra )
classroom.drop(labels = [0, 1], inplace = True)
# Đoạn này cũng cần kiểm tra lại, xóa lần nữa cho chắc 
class_room = classroom.dropna(axis = 0, how = 'all')
# Reset lại index của 
class_room = class_room.reset_index(drop = True)
# In ra danh sách 
print(class_room)
