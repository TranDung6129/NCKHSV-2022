import os
import pandas as pd
import numpy as np

class Classroom:
    
    def __init__(self):
        '''Em chưa nghĩ ra cách để chỉ chạy mà không cần làm gì cả, thế nên trước mắt thì sẽ giải quyết 
        bằng cách là để người sử dụng về sau tự nhập thông tin cột, em sẽ nghĩ cách để tự động hết sau ạ'''
        filepath = input("Xin mời nhập đường dẫn tới file: ")
        
        # Lựa chọn biểu đồ chứa danh sách phòng học
        self.df = pd.read_excel(filepath, sheet_name = 'BIỂU ĐỒ (S)')
            
        # Tên của cột Số phòng mới và Số chỗ
        self.df_column = input("Tên cột chứa danh sách phòng học là: ")
        self.df_capacity = input("Tên của cột chứa sức chứa của các phòng học là: ")
        
        # Xử lý và làm sạch dữ liệu
        
        self.df = self.df[[self.df_column, self.df_capacity]]
        
        # Xóa tất cả các hàng chứa toàn bộ dữ liệu trống
        self.df.dropna(axis = 0, how = 'all')
        # Đổi tên cột để phù hợp với mô tả của mô hình 
        self.df.rename(columns = {self.df_column: 'Tên phòng', self.df_capacity: 'Sức chứa'}, inplace = True)
        
        # Xóa hai cột trống phía trên (đoạn này cần kiểm tra)
        self.df.drop(labels = [0, 1], inplace = True)
        
        # Đoạn này cũng cần kiểm tra lại, xóa lần nữa cho chắc
        self.df = self.df.dropna(axis = 0, how = 'all')
        
        # Thay các giá trị NaN thành 0 để tiện cho việc so sánh về sau
        self.df = self.df.fillna(0)
         
        # Reset lại index của bảng
        self.df = self.df.reset_index(drop = True)
        
    def get_table(self):
        '''In ra dataframe chứa tên và sức chứa của các phòng'''
        return f"Dưới đây là danh sách phòng học và sức chứa của phòng: \n\n {self.df}"
        
    def get_available__classroom_number(self):
        '''In ra số lượng phòng có thể sử dụng'''
        self.df = self.df.apply(lambda x : True if x['Sức chứa'] != 0 else False, axis=1)
        return f"Số phòng có thể sử dụng là: {self.df.shape[0]}"
    
    def get_classroom_capacity(self, classroom_name):
        '''Lấy sức chứa của từng phòng học theo xác định. 
        classroom_name= ('tên của phòng học muốn lấy sức chứa')'''
        self.df.set_index("Tên phòng", inplace = True)
        return self.df.loc[classroom_name]["Sức chứa"]
        
