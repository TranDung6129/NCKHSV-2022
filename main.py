import os
import pandas as pd
import numpy as np
from classroom import Classroom
from information import ClassInformation
from gurobipy import *
import itertools

'''Nhập đường dẫn và cột không tên là em chưa nghĩ ra hướng giải quyết phù hợp, 
em dự định sử dụng file nhưng thử mãi chưa dùng được nên chị có thể kiểm tra giúp
em xem có phù hợp không nếu không thì sẽ nghĩ cách khác ạ'''
'''Ở trên là cách giải quyết đường dẫn như nhập file Excel nhưng còn cột không được 
đặt tên thì em vẫn chưa nghĩ ra cách giải quyết ạ'''


milp_model = Model(name="milp")
variable = []

classroom = Classroom()
classroom_df = classroom.df
information = ClassInformation()
information_df = information.df
'''Trích xuất các thông tin cần thiết của mô hình'''
# Tập A gồm n mã lớp sẽ mở trong kỳ xếp thời khóa biểu 
A_set = [] 
for class_code in information.get_class_code():
    A_set.append(class_code)
    
# Tập C gồm p lớp theo chương trình đào tạo 
class_extract = []
class_name_by_class_code = [] 
for class_code in A_set:
    class_name = information.get_participant_class(class_code)
    class_name_by_class_code.append(class_name)
class_extract = list(itertools.chain.from_iterable(class_name_by_class_code))

C_set = []
for class_name in class_extract:
    if class_name not in C_set:
        C_set.append(class_name)
print(C_set)
# Tập F là số sinh viên của từng mã lớp
F_set = []
for class_code in A_set:
    class_number = information.get_student_number(class_code)
    F_set.append(class_number)
    
# Tập H là thời lượng tính theo tiết của các mã lớp mỗi tuần 
H_set = []
for class_code in A_set:
    class_periods = information.get_class_periods_number(class_code)
    H_set.append(class_periods)

# Tập B là m mã phòng hiện có ở tòa D7 
B_set = []
for classroom_name in classroom.get_class_room_list():
    B_set.append(classroom_name)

# Tập D là sức chứa của các phòng tương ứng với mã phòng:
D_set = []
for classroom_name in B_set:
    D_set.append(classroom.get_classroom_capacity(classroom_name))

# =============================================================================
# Nhập ma trận G là ma trận biểu thị các lớp chia theo chương trình đào tạo.
# Hàng của ma trận ứng với các lớp trong chương trình đào tạo
# Cột của ma trận ứng với các mã lớp mở trong kỳ
# Khởi tạo ma trận chứa tất cả các ô là 0, lấy số cột của ma trận và số hàng của
# ma trận


# =============================================================================
'''Tạo ra các biến của mô hình'''
# Tạo biến nhị phân x_m, thể hiện rằng phòng thứ m có được sử dụng hay không

# Tạo biến nhị phân y_nm, thể hiện rằng mã lớp n được xếp vào phòng thứ m 

# Tạo biến u_n, là tiết học bắt đầu của lớp thứ n 

# Tạo biến a_nti nếu mã lớp thứ n bắt đầu từ tiết thứ i của buổi t. i chạy trong tập 
# {1, 2,..., 10} 
'''Đưa vào các hàm mục tiêu của mô hình'''
# Số phòng được sử dụng ít nhất

# Số buổi có tiết học trong tuần của một lớp chia theo chương trình đào tạo là ít nhất

# Trong cùng một buổi học các lớp ưu tiên không cần phải di chuyển giữa các phòng

'''Đưa vào các ràng buộc của mô hình''' 
# Mỗi mã lớp chỉ được xếp vào một phòng duy nhất

# Mỗi mã lớp chỉ được xếp vào một buổi học (thời gian bắt đầu và kết thúc phải cùng 
# một buổi)

# Mỗi mã lớp chỉ xếp vào buổi học duy nhất

# Sức chứa của phòng học lớn hown sĩ số của mã lớp được xếp vào phòng đó

# Lịch học của các mã lớp con không được trùng nhau

