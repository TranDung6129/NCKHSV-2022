import os
import pandas as pd
import numpy as np

class ClassInformation:
    
    def __init__(self):
        filepath = 'D:/Nhóm nghiên cứu/Nghiên cứu ứng dụng/Bài toán lập lịch/TKB-SIE-ky-20212-14.4.22.xlsx'
        # Điền ký học hiện tại, là đối số của tên sheet chọn bên dưới 
        semester = 20212 
        # Lấy sheet chứa kế hoạch kì 20212
        self.df = pd.read_excel(filepath, sheet_name = f'Báo dạy {semester}')
        
        # Xóa các cột và các hàng chứa toàn bộ các giá trị là NaN
        self.df = self.df.dropna(axis = 0, how = 'all')
        self.df = self.df.dropna(axis = 1, how = 'all')
        
        # Đưa toàn bộ tên cột vào một list
        columns_name_list = list(self.df.columns)
        
        # Lấy số lượng cột 
        number_of_columns = len(self.df.columns)
        
        ''' Đổi tên lại toàn bộ các cột (ở cột cuối thì do cô ghi vài thứ vào nên em không biết nên xóa hay không, 
        vậy nên cả cái cột nó toàn NaN nhưng mà thực ra là có hai cột chứa dữ liệu, em  nghĩ là xóa đi rồi tạo hẳn 
        phần ghi chú cho chương trình lúc làm sau này ạ)'''
        for i in range(number_of_columns):
            self.df.rename(columns = {f'{columns_name_list[i]}': f"{self.df.iloc[0][columns_name_list[i]]}"}, inplace = True)
            
        # Xóa cột chứa tên cột ban đầu 
        self.df.drop(labels = 1, axis = 0, inplace = True)
        
        # Reset lại index của cột  
        self.df = self.df.reset_index(drop = True)
        
        # Thêm cột mã lớp
        new_class_code = []
        self.df['STT theo mã HP'] = self.df['STT theo mã HP'].astype(str).str.zfill(3)
        number_code = self.df["STT theo mã HP"].tolist()
        for i in number_code:
            new_code = "134" + str(i)
            new_class_code.append(new_code)
        self.df.insert(0, "Mã lớp", new_class_code, True)
            
    def get_table(self):
        '''In ra màn hình bảng chứa thông tin'''
        return self.df
    
    def get_student_number(self, class_code):
        ''' Trả về số sinh viên từng mã lớp.
        class_code = ('Mã lớp')'''
        class_index = self.df.index[self.df['Mã lớp'] == class_code].astype(int)[0]
        return self.df.at[class_index, 'Số SV lớp cố định']

    def get_class_periods_number(self, class_code):
        '''Trả về số tiết học của một mã lớp trong kỳ, dựa vào khối lượng'''
        period_index = self.df.index[self.df['Mã lớp'] == class_code].astype(int)[0]
        periods_retrieve = self.df.at[period_index, 'KHỐI LƯỢNG ']
        periods_retrieve = str(periods_retrieve)
        if periods_retrieve == "" or periods_retrieve == "nan":
            periods_retrieve = "0(_______)"
        if len(periods_retrieve) == 1:
            periods_retrieve = str(periods_retrieve[0]) + "(_______)"
        if str(periods_retrieve)[1] == "(":
            periods = str(periods_retrieve)[0]
        else:
            periods = str(periods_retrieve)[0:2]
        return periods
    
    def get_participant_class(self, class_code):
        '''Trả về tên của các lớp con tham gia một mã lớp'''
        participant_class_index  = self.df.index[self.df['Mã lớp'] == class_code].astype(int)[0]
        participant_class = self.df.at[participant_class_index, "Lớp"]
        participant_class_list = list(participant_class.split("+"))
        for i in participant_class_list:
            if i == 'B':
                B_index = participant_class_list.index('B')
                participant_class_list[B_index - 1] = participant_class_list[B_index - 1] + "+" + participant_class_list[B_index]
                participant_class_list.remove("B")
        return participant_class_list
    
    def get_class_code(self):
        class_code = self.df["Mã lớp"].to_list()
        return class_code
