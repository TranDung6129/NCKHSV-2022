import os
import pandas as pd
import numpy as np
from classroom import Classroom
from information import ClassInformation
import pyomo.environ as pyo
from pyomo.environ import * 
import itertools

'''Nhập đường dẫn và cột không tên là em chưa nghĩ ra hướng giải quyết phù hợp, 
em dự định sử dụng file nhưng thử mãi chưa dùng được nên chị có thể kiểm tra giúp
em xem có phù hợp không nếu không thì sẽ nghĩ cách khác ạ'''
'''Ở trên là cách giải quyết đường dẫn như nhập file Excel nhưng còn cột không được 
đặt tên thì em vẫn chưa nghĩ ra cách giải quyết ạ'''

# model
model = pyo.ConcreteModel()

classroom = Classroom()
classroom_df = classroom.df
information = ClassInformation()
information_df = information.df
'''Trích xuất các thông tin cần thiết của mô hình'''
# Tập A gồm n mã lớp sẽ mở trong kỳ xếp thời khóa biểu 
A_set = [] 
for class_code in information.get_class_code():
    A_set.append(class_code)
nA = len(A_set)
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
nC = len(C_set)
# Tập F là số sinh viên của từng mã lớp
F_set = []
for class_code in A_set:
    class_number = information.get_student_number(class_code)
    F_set.append(class_number)
nF = len(F_set)
# Tập H là thời lượng tính theo tiết của các mã lớp mỗi tuần 
H_set = []
for class_code in A_set:
    class_periods = information.get_class_periods_number(class_code)
    H_set.append(class_periods)
nH = len(H_set)
# Tập B là m mã phòng hiện có ở tòa D7 
B_set = []
for classroom_name in classroom.get_class_room_list():
    B_set.append(classroom_name)
nB = len(B_set)
# Tập D là sức chứa của các phòng tương ứng với mã phòng:
D_set = []
for classroom_name in B_set:
    D_set.append(classroom.get_classroom_capacity(classroom_name))
nD = len(D_set)
# =============================================================================
# Nhập ma trận G là ma trận biểu thị các lớp chia theo chương trình đào tạo.
# Hàng của ma trận ứng với các lớp trong chương trình đào tạo
# Cột của ma trận ứng với các mã lớp mở trong kỳ
# Khởi tạo ma trận chứa tất cả các ô là 0, lấy số cột của ma trận và số hàng của
# ma trận
matrix_column_number = len(C_set)
matrix_row_number = len(A_set)
G_matrix = np.zeros((matrix_row_number, matrix_column_number))

#==============================================================================
'''Tạo ra các biến của mô hình'''
# Tạo biến nhị phân x_m, thể hiện rằng phòng thứ m có được sử dụng hay không
model.x = pyo.Var(range(nB), bounds=(0, 1), initialize=(0), within=Binary)
x_m = model.x
# Tạo biến nhị phân y_nm, thể hiện rằng mã lớp thứ n được xếp vào phòng thứ m 
model.y = pyo.Var(range(nA), range(nB), bounds=(0, 1), initialize=(0), within=Binary)
y_nm = model.y
# Tạo biến u_n, là tiết học bắt đầu của lớp thứ n 
model.u = pyo.Var(range(nA), bounds=(1, 6), domain=Integers)
u_n = model.u
# Tạo biến t là buổi học trong tuần (từ thứ 2 đến thứ 6, sáng và chiều)
model.t = pyo.Var(bounds=(1, 10), domain=Integers)
t = model.t
# Tạo biến a_nti nếu mã lớp thứ n bắt đầu từ tiết thứ i của buổi t. 
model.a = pyo.Var(range(nA), range(1, 7), range(1, 11), bounds=(0, 1), initialize=(0), within=Binary)
a_nti = model.a
# Biến p_t = 1 nếu lớp p học vào buổi thứ t và p_t = 0 nếu ngược lại
model.p = pyo.Var(bounds=(0, 1), initialize=(0), within=Binary)
'''Đưa vào các ràng buộc của mô hình''' 
# Mỗi mã lớp chỉ được xếp vào một phòng duy nhất
model.class_limit = pyo.ConstraintList()
for n in range(nA):
    y_nm_sum = sum([y_nm[n, m] for m in range(nB)])
    model.class_limit.add(expr = y_nm_sum <= 1)
# Mỗi mã lớp chỉ được xếp vào một buổi học (thời gian bắt đầu và kết thúc phải cùng 
# một buổi)
# =============================================================================
# model.in_1_session = pyo.ConstraintList()
# for n in range(nA):
#     for h_n in H_set:
#         model.in_1_session.add(expr = u_n[n] + h_n[n] - 1 <= 6)
# =============================================================================
# Mỗi mã lớp chỉ xếp vào buổi học duy nhất

# Sức chứa của phòng học lớn hơn sĩ số của mã lớp được xếp vào phòng đó

# Lịch học của các mã lớp con không được trùng nhau


'''Đưa vào các hàm mục tiêu của mô hình'''
# Số phòng được sử dụng ít nhất
model.obj1 = pyo.Objective(expr = sum([x_m[m] for m in range(nB)]), sense=minimize)
# Số buổi có tiết học trong tuần của một lớp chia theo chương trình đào tạo là ít nhất

# Trong cùng một buổi học các lớp ưu tiên không cần phải di chuyển giữa các phòng

'''Xử lý mô hình'''
opt = SolverFactory('cplex')
results = opt.solve(model)
