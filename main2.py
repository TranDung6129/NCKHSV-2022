import os
import pandas as pd
import numpy as np
from classroom import Classroom
from information import ClassInformation
import pyomo.environ as pyo
from pyomo.environ import * 
import itertools
import time as t

# model
model = pyo.ConcreteModel()
# Điều chỉnh DataFrame 
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
    H_set.append(int(class_periods))
for class_periods_ in H_set:
    if class_periods_ >= 6:
        class_periods_ = 0
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
# Nhập ma trận K là ma trận biểu thị các lớp chia theo chương trình đào tạo.
# Cột của ma trận ứng với các lớp trong chương trình đào tạo
# Hàng của ma trận ứng với các mã lớp mở trong kỳ
# Khởi tạo ma trận chứa tất cả các ô là 0, lấy số cột của ma trận và số hàng của
# ma trận
K_matrix = np.zeros((nA, nC))
for class_code in A_set:
	class_list = information.get_participant_class(class_code)
	for class_name in class_list:
		class_index = C_set.index(class_name)
		K_matrix[A_set.index(class_code), class_index] = 1
        
'''Tạo ra các biến của mô hình'''
# Tạo biến nhị phân x_m, thể hiện rằng phòng thứ m có được sử dụng hay không
model.x = pyo.Var(B_set, bounds=(0, 1), initialize=(0), within=Binary)
x_m = model.x
# Tạo biến nhị phân y_nm, thể hiện rằng mã lớp thứ n được xếp vào phòng thứ m 
model.y = pyo.Var(A_set, B_set, bounds=(0, 1), initialize=(0), within=Binary)
y_nm = model.y
# Biến v_nmti là mã lớp thứ n được xếp vào phòng học thứ m vào buổi t, bắt đầu vào tiết i
model.v = pyo.Var(A_set, B_set, range(1, 11), range(1, 7), bounds=(0, 1), within=Integers)
v_nmti = model.v
# Tạo các biến nhị phân y1
model.y1 = pyo.Var(bounds=(0, 1), within=Binary)
y1 = model.y1

'''Đưa vào các ràng buộc của mô hình'''
# Ràng buộc 1
model.constraint_1 = pyo.ConstraintList()
for n in A_set:
    y_nm_components = []
    for m in B_set:
        y_nm_components.append(y_nm[n, m])
        y_nm_sum = sum(y_nm_components)
    model.constraint_1.add(expr= y_nm_sum == 1)

# Ràng buộc 2 
model.constraint_2 = pyo.ConstraintList()
for m in B_set:
    y_nm_n = []
    for n in A_set:
        y_nm_n.append(y_nm[n, m])
        y_nm_n_sum = sum(y_nm_n)
    model.constraint_2.add(expr= y_nm_n_sum <= nA * x_m[m])
    
# Ràng buộc 3 
model.constraint_3 = pyo.ConstraintList()
for n in A_set:
    v_nmti_sum = []
    for m in B_set:
        for t in range(1, 11):
            for i in range(1, 7):
                v_nmti_sum.append(v_nmti[n, m, t, i])
    model.constraint_3.add(expr= sum(v_nmti_sum) <= H_set[A_set.index(n)] * y_nm[n, m])
# Ràng buộc 4
model.constraint_4 = pyo.ConstraintList()
for n in A_set:
    for m in B_set:
        model.constraint_4.add(expr= F_set[A_set.index(n)] * y_nm[n, m] <= D_set[B_set.index(m)] * x_m[m])
# Ràng buộc 5
model.constraint_5 = pyo.ConstraintList()
for n in A_set:
    v_nmti_sum5 = []
    for t in range(1, 11):
        for i in range(1, 7):
            for m in B_set:
                v_nmti_sum5.append(v_nmti[n, m, t, i])
        model.constraint_5.add(expr= sum(v_nmti_sum5) <= H_set[A_set.index(n)] * y1)
        model.constraint_5.add(expr= H_set[A_set.index(n)] - sum(v_nmti_sum5) <= 2 * H_set[A_set.index(n)] * (1 - y1))
# Ràng buộc 6
# model.constraint_6 = pyo.ConstraintList()
# for n in A_set:
#     for m in B_set:
#         for t in range(1, 11):
#             v_nmti_sum6 = []
#             for p in range(1, 7):
#                 periods_range = p + H_set[A_set.index(n)] - 1
#                 if periods_range <= 6:
#                     for i in range(p, periods_range + 1):
#                         v_nmti_sum6.append(v_nmti[n, m, t, i])
#     model.constraint_6.add(expr= sum(v_nmti_sum6) <= H_set[A_set.index(n)])
# # Ràng buộc 7
model.constraint_7 = pyo.ConstraintList()
for m in B_set:
    for t in range(1, 11):
        for i in range(1, 7):
            v_nmti_cns7_sum = []
            for n in A_set:
                v_nmti_cns7_sum.append(v_nmti[n, m, t, i])
            model.constraint_7.add(expr= sum(v_nmti_cns7_sum) <= 1)
'''Đưa vào các hàm mục tiêu của mô hình'''
model.obj1 = pyo.Objective(expr= sum([x_m[m] for m in B_set]), sense=minimize)

'''Xử lý mô hình'''
opt = SolverFactory('cplex')
results = opt.solve(model) 
