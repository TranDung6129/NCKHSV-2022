import os
import pandas as pd
import numpy as np
from classroom import Classroom
from information import ClassInformation
import pyomo.environ as pyo
from pyomo.environ import * 
import itertools
import time as t

'''Nhập đường dẫn và cột không tên là em chưa nghĩ ra hướng giải quyết phù hợp, 
em dự định sử dụng file nhưng thử mãi chưa dùng được nên chị có thể kiểm tra giúp
em xem có phù hợp không nếu không thì sẽ nghĩ cách khác ạ'''
'''Ở trên là cách giải quyết đường dẫn như nhập file Excel nhưng còn cột không được 
đặt tên thì em vẫn chưa nghĩ ra cách giải quyết ạ'''

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
# Hàng của ma trận ứng với các lớp trong chương trình đào tạo
# Cột của ma trận ứng với các mã lớp mở trong kỳ
# Khởi tạo ma trận chứa tất cả các ô là 0, lấy số cột của ma trận và số hàng của
# ma trận
# =============================================================================
# index = information.df.index
# for class_code in A_set:
#     condition = information.df["Mã lớp"] == class_code
#     number_of_classes = len(information.get_participant_class(class_code))
#     for i in range(1, number_of_classes + 1):
#         information.df.at[index[condition], f"class1_{i}"] = information.get_participant_class(class_code)[i - 1]
# =============================================================================

K_matrix = np.zeros((nA, nC))
for class_code in A_set:
	class_list = information.get_participant_class(class_code)
	for class_name in class_list:
		class_index = C_set.index(class_name)
		K_matrix[A_set.index(class_code), class_index] = 1

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
# =============================================================================
# # Tạo biến t là buổi học trong tuần (từ thứ 2 đến thứ 6, sáng và chiều)
# model.t = pyo.Var(bounds=(1, 10), domain=Integers)
# t = model.t
# =============================================================================

# Tạo biến a_nti nếu mã lớp thứ n bắt đầu từ tiết thứ i của buổi t. 
model.a = pyo.Var(range(nA), range(1, 11), range(1, 7), bounds=(0, 1), initialize=(0), within=Integers)
a_nti = model.a
# Biến P_pt = 1 nếu lớp p học vào buổi thứ t và p_t = 0 nếu ngược lại
model.P = pyo.Var(range(nC), range(1, 11), bounds=(0, 1), initialize=(0), within=Integers)
P_pt = model.P
# Biến v_nmti là mã lớp thứ n được xếp vào phòng học thứ m vào buổi t, bắt đầu vào tiết i
model.v = pyo.Var(range(nA), range(nC), range(1, 11), range(1, 7), bounds=(0, 1), initialize=(0), within=Integers)
v_nmti = model.v
# Biến q_npt là mã lớp n có lớp con p học vào buổi t
model.q = pyo.Var(range(nA), range(nC), range(1, 11), bounds=(0, 1), initialize=(0), within=Integers)
q_npt = model.q
# Tạo các biến nhị phân y1, y2, y3
model.y1 = pyo.Var(bounds=(0, 1), initialize=(0), within=Binary)
y1 = model.y1
model.y2 = pyo.Var(bounds=(0, 1), initialize=(0), within=Binary)
y2 = model.y2
model.y3 = pyo.Var(bounds=(0, 1), initialize=(0), within=Binary)
y3 = model.y3
'''Đưa vào các ràng buộc của mô hình'''
# Mỗi mã lớp chỉ được xếp vào một phòng duy nhất
model.class_limit = pyo.ConstraintList()
for n in range(nA):
    y_nm_sum = sum([y_nm[n, m] for m in range(nB)])
    model.class_limit.add(expr= y_nm_sum == 1)
# Ràng buộc 2
model.const2 = pyo.ConstraintList()
for m in range(nB):
    y_nm_sum2 = sum(y_nm[n, m] for n in range(nA))
    model.const2.add(expr= y_nm_sum2 <= 10000  * x_m[m]) 
# Mỗi mã lớp chỉ xếp vào buổi học duy nhất
model.each_class_unique_session = pyo.ConstraintList()
for n in range(nA):
    for t in range(1, 11):
        a_nti_sum = sum([a_nti[n, t, i] for i in range(1, 7)])
        model.each_class_unique_session.add(expr= a_nti_sum == 1)
# Ràng buộc thứ 4
model.const4 = pyo.ConstraintList()
for n in range(nA):
    for p in range(nC):
        for t in range(1, 11):
            a_nti_sum4 = []
            for i in range(1, 7):
                a_nti_sum4.append(a_nti[n, t, i])
            a_nti_sum4 = sum(a_nti_sum4)
            model.const4.add(expr= q_npt[n, p, t] <= 10000 * (1 - y1))
            model.const4.add(expr= a_nti_sum <= 10000 * y1)
# Ràng buộc thứ 5
model.const5 = ConstraintList()
for n in range(nA):
    for i in range(1, 7):
        a_nti_sum5 = []
        for t in range(1, 11):
            a_nti_sum5.append(a_nti[n, t, i])
        a_nti_sum5 = sum(a_nti_sum5)
        model.const5.add(expr= a_nti_sum5 <= 10000 * (1 - y2))
        model.const5.add(expr= u_n[n] - i <= 100 * y2)
# Ràng buộc thứ 6
"""Đã được định nghĩa ngay trong biến"""
# Ràng buộc thứ 7
model.in_1_session = pyo.ConstraintList()
for n in range(nA):
    for h_n in H_set:
        model.in_1_session.add(expr = u_n[n] + h_n - 1 <= 6)
# Ràng buộc thứ 8
model.const8 = pyo.ConstraintList()
for n in range(nA):
    for t in range(1, 11):
        for i in range(1, 7):
            v_nmti_sum =[]
            for m in range(nB):
                v_nmti_sum.append(v_nmti[n, m, t, i])
            v_nmti_sum = sum(v_nmti_sum)
            model.const8.add(expr= v_nmti_sum <= a_nti[n, t, i])
# Ràng buộc thứ 9
model.const9 = pyo.ConstraintList()
for n in range(nA):
    for m in range(nB):
        v_nmti_sum = []
        for t in range(1, 11):
            for i in range(1, 7):
                v_nmti_sum.append(v_nmti[n, m, t, i])
        v_nmti_sum = sum(v_nmti_sum)
        model.const9.add(expr= v_nmti_sum <= y_nm[n, m])
# Ràng buộc thứ 10
model.const10 = ConstraintList()

# Ràng buộc thứ 11
model.const11 = pyo.ConstraintList()
for p in range(nC):
    for t in range(1, 11):
        q_npt_sum = []
        for n in range(nA):
            q_npt_sum.append(q_npt[n, p, t])
        q_npt_sum = sum(q_npt_sum)
        model.const11.add(expr= q_npt_sum <= 10000 * P_pt[p, t])
# Ràng buộc thứ 12
model.const12 = pyo.ConstraintList()
for p in range(nC):
    for n in range(nA):
        q_npt_sum = []
        for t in range(1, 11):
            q_npt_sum.append(q_npt[n, p, t])
        q_npt_sum = sum(q_npt_sum)
        model.const12.add(expr= q_npt_sum <= 2)
# Ràng buộc thứ 13
model.const13 = pyo.ConstraintList()
for n in range(nA):
    for m in range(nB):
        model.const13.add(expr= F_set[n] * y_nm[n, m] <= 0.9 * D_set[m] * x_m[m])
'''Đưa vào các hàm mục tiêu của mô hình'''
# Số phòng được sử dụng ít nhất
model.obj1 = pyo.Objective(expr= sum([x_m[m] for m in range(nB)]), sense=minimize)
# Số buổi có tiết học trong tuần của một lớp chia theo chương trình đào tạo là ít nhất
P_pt_sum = []
for p in range(nC):
    for t in range(1, 11):
        P_pt_sum.append(P_pt[p, t])
P_pt_sum = sum(P_pt_sum)
model.obj2 = pyo.Objective(expr= P_pt_sum, sense=minimize)
# Trong cùng một buổi học các lớp ưu tiên không cần phải di chuyển giữa các phòng


'''Xử lý mô hình'''
opt = SolverFactory('cplex')
opt.solve(model)

