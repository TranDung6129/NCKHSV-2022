import os
import pandas as pd
import numpy as np


filepath = input("Xin mời nhập đường dẫn tới file: ")
basename = os.path.basename(filepath)
print(basename)


# Lấy sheet chứa kế hoạch kì 20212, đoạn này nếu sửa thì em định cho kì học là biến còn lại giữ nguyên thì những kì sau chỉ cần nhập kì học thôi
class_open_plan = pd.read_excel(filepath, sheet_name = 'Báo dạy 20212')


# Xóa các cột và các hàng chứa toàn bộ các giá trị là NaN
class_open_plan = class_open_plan.dropna(axis = 0, how = 'all')
class_open_plan = class_open_plan.dropna(axis = 1, how = 'all')


# Đưa toàn bộ tên cột vào một list
columns_name_list = list(class_open_plan.columns)


# Lấy số lượng cột 
number_of_columns = len(class_open_plan.columns)


# Đổi tên lại toàn bộ các cột
for i in range(number_of_columns):
    class_open_plan.rename(columns = {f'{columns_name_list[i]}': f"{class_open_plan.iloc[0][columns_name_list[i]]}"}, inplace = True)

    
# Xóa cột chứa tên cột ban đầu 
class_open_plan.drop(labels = 1, axis = 0, inplace = True)


# Reset lại index của cột  
class_open_plan = class_open_plan.reset_index(drop = True)


print(class_open_plan)
