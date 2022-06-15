import os
import pandas as pd
import numpy as np
from classroom import Classroom
from information import ClassInformation
import pyomo.environ as pyo
from pyomo.environ import * 
import itertools
from pyomo.opt import SolverStatus, TerminationCondition
from functools import reduce
from time import time

start_time = time()
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
for i in range(len(H_set)):
    if H_set[i] > 4:
        H_set[i] = 0
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

# Tập hợp STT theo mã HP
STT_set = []
for class_code_order in information.get_class_code_order():
    STT_set.append(class_code_order)
# Tập hợp chứa các lớp ghép 
G_set = []
for class_code_order in STT_set:
    G_set.append(information.get_class_group(class_code_order))
unique_list = []
for _ in G_set:
    if _ not in unique_list:
        unique_list.append(_)
G_set = unique_list
g_set = []
for class_code_order in STT_set:
    g_set.append(information.get_class_group(class_code_order))

# dict_1
# def get_dict_1():
#     group_class_list = []
#     for class_code in A_set:
#         group_class_list.append(information.get_participant_class(class_code))
#     # Dictionary, key là mã lớp, value là nhóm các lớp con tham gia vào mã lớp đó
#     dict_1 = {}
#     for class_code in A_set:
#         for group_class in group_class_list:
#             dict_1[class_code] = group_class
#             group_class_list.remove(group_class)
#             break
#     return dict_1
# # dict_2
# list_code_course = {}
# for j in range(len(G_set)):
#     temp_list = []
#     for i in range(len(information_df)):
#         if information_df.iloc[i, 7] == G_set[j]:
#             temp_list.append(information_df.iloc[i, 0])
#     list_code_course[G_set[j]] = temp_list

# # dict_3
# def get_dict_3():
#     list_student_number = {}
#     for group_class in G_set:
#         for student_number in F_set:
#             list_student_number[group_class] = student_number
#             F_set.remove(student_number)
#             break
#     return list_student_number

# for group_class in G_set
'''Tạo ra các biến của mô hình'''
model.v = pyo.Var(range(1, 11), range(1, 7), g_set, A_set, B_set, initialize=(0), within=Binary)
v_tignm = model.v

model.y = pyo.Var(A_set, B_set, H_set, range(1, 11), initialize=(0), within=Binary)
y_nmht = model.y

model.a = pyo.Var(B_set, initialize=(0), within=Binary)
a_m = model.a

'''Đưa vào các ràng buộc của mô hình'''
# Ràng buộc 1: Mỗi nhóm lớp tại một thời điểm chỉ học tối đa một mã lớp tại một phòng học duy nhất
model.constraint_1 = pyo.ConstraintList()
for t in range(1, 11):
    v_tignm_components = []
    for i in range(1, 7):
        for m in B_set:
            for n in range(len(A_set)):
                v_tignm_components.append(v_tignm[t, i, g_set[n], A_set[n], m])
            v_tignm_sum = sum(v_tignm_components)
        model.constraint_1.add(expr=v_tignm_sum <= 1)
# Ràng buộc 2: Tại một thời điểm mỗi phòng chỉ có tối đa mã lớp học được học bởi một nhóm lớp
model.constraint_2 = pyo.ConstraintList()
for m in B_set:
    for t in range(1, 11):
        for i in range(1, 7):
            v_tignm_components = []
            for g in g_set:
                v_tignm_components.append(v_tignm[t, i, g, A_set[g_set.index(g)], m])
                v_tignm_sum = sum(v_tignm_components)
                model.constraint_2.add(expr=v_tignm_sum <= 1)
# Ràng buộc 3: Mỗi mã lớp học phải được xếp đủ số tiết học 
model.constraint_3 = pyo.ConstraintList()
for g in g_set:
    v_tignm_components = []
    for m in B_set:
        for t in range(1, 11):
            for i in range(1, 7):
                v_tignm_components.append(v_tignm[t, i, g, A_set[g_set.index(g)], m])
                v_tignm_sum = sum(v_tignm_components)
                model.constraint_3.add(expr=v_tignm_sum <= H_set[g_set.index(g)])
# Ràng buộc 4: Các tiết học của một mã lớp phải học trong cùng một phòng 
model.constraint_4 = pyo.ConstraintList()
for n in A_set:
    for m in B_set:
        v_tignm_components_1 = []
        v_tignm_components_2 = []
        for t in range(1, 11):
            for i in range(1, 7):
                v_tignm_components_1.append(v_tignm[t, i, g_set[A_set.index(n)], n, m])
                v_tignm_1_sum = sum(v_tignm_components_1)
                v_tignm_components_2.append(v_tignm[t, i, g_set[A_set.index(n)], n, m])
                v_tignm_2_sum = sum(v_tignm_components_2)
                model.constraint_4.add(expr=H_set[A_set.index(n)] * v_tignm_2_sum <= v_tignm_1_sum)
                
# Ràng buộc 5: Mỗi lớp con tại 1 thời điểm chỉ học tối đa 1 mã lớp tại 1 phòng 

# Ràng buộc 6: Các tiết học của 1 mã lớp phải trong cùng 1 buổi 
model.constraint_6 = pyo.ConstraintList()
for n in A_set:
    v_tignm_components = []
    for m in B_set:
        for t in range(1, 11):
            for i in range(1, 7):
                v_tignm_components.append(v_tignm[t, i, g_set[A_set.index(n)], n, m])
            v_tignm_sum = sum(v_tignm_components)
            model.constraint_6.add(expr=v_tignm_sum == H_set[A_set.index(n)] * y_nmht[n, m, H_set[A_set.index(n)], t])
# Ràng buộc 7: Số tiết học sử dụng phòng p trong 1 tuần không vượt quá 60 tiết
model.constraint_7 = pyo.ConstraintList()
for m in B_set:
    v_tignm_components = []
    for t in range(1, 11):
        for i in range(1, 7):
            for n in A_set:
                v_tignm_components.append(v_tignm[t, i, g_set[A_set.index(n)], n, m])
                v_tignm_sum = sum(v_tignm_components)
                model.constraint_7.add(expr=a_m[m] <= v_tignm_sum)
                model.constraint_7.add(expr=v_tignm_sum <= 60 * a_m[m])
                
# Ràng buộc 8: Các tiết học của một mã lớp phải được xếp liên tiếp nhau 
model.constraint_8 = pyo.ConstraintList()
for n in A_set:
    for m in B_set:
        for t in range(1, 11):
            for k in range(1, H_set[A_set.index(n)]):
                model.constraint_8.add(expr=v_tignm[t, 1, g_set[A_set.index(n)], n, m] <= v_tignm[t, k + 1, g_set[A_set.index(n)], n, m])
for n in A_set:
    for m in B_set:
        for t in range(1, 11):
            for i in range(1, 6):
                for k in range(2, H_set[A_set.index(n)]):
                    if i + k <= 6:
                        model.constraint_8.add(expr=v_tignm[t, i + 1, g_set[A_set.index(n)], n, m] <= v_tignm[t, i, g_set[A_set.index(n)], n, m] + v_tignm[t, i + k, g_set[A_set.index(n)], n, m])

# Ràng buộc 9: Các biến v khác 0
model.constraint_9 = pyo.ConstraintList()
v_tignm_set = []
for key in model.v:
    v_tignm_set.append(model.v[key])
model.constraint_9.add(expr=sum(v_tignm_set) >= 10)
'''Đưa vào các hàm mục tiêu của mô hình'''
model.obj1 = pyo.Objective(expr= sum([a_m[m] for m in B_set]), sense=pyo.minimize)

'''Xử lý mô hình'''
opt = SolverFactory('cplex')
# opt.options['timelimit'] = 1
results = opt.solve(model, tee=True) 

optimal_values = [pyo.value(model.v[key]) for key in model.v]
df = pd.DataFrame(optimal_values)

end_time = time()
time = end_time - start_time
'''Xuất dữ liệu đã được tối ưu ra file Excel'''
# Tên học phần học tại các mã lớp 
credit_name_list = []
for class_code in range(len(A_set)):
    credit_name_list.append(information_df.at[class_code, "TÊN HP"])
    
# Mã học phần học tại các mã lớp 
credit_code_list = []
for class_code in range(len(A_set)):
    credit_code_list.append(information_df.at[class_code, "MÃ HP"])

# Lấy sĩ số của mỗi mã lớp 
class_population_list = []
for class_code in range(len(A_set)):
    class_population_list.append(information_df.at[class_code, "Số SV lớp cố định"])


# Lấy buổi học từ kết quả tối ưu
# def get_study_half(optimal_data):
#     '''Lấy buổi học theo từ kết quả tối ưu'''
#     result = ''
#     if (optimal_data[0]) % 2 == 0:
#         result = 'Chiều'
#     else:
#         result = 'Sáng'
# Danh sách chứa key các đầu ra 
key_list = []
for key in model.v:
    if pyo.value(model.v[key]) != 0:
        key_list.append(key)
        
        
study_day = [2, 3, 4, 5, 6]
study_half_day = ["Sáng", "Chiều"]
study_time_dict = {"Thứ": study_day, "Kíp": study_half_day}

study_day_output = []
study_half_day_output = []

def get_day(optimal_data):
    if optimal_data[0] == 1 or optimal_data[0] == 2:
        return 2
    if optimal_data[0] == 3 or optimal_data[0] == 4:
        return 3
    if optimal_data[0] == 5 or optimal_data[0] == 6:
        return 4
    if optimal_data[0] == 7 or optimal_data[0] == 8:
        return 5
    if optimal_data[0] == 9 or optimal_data[0] == 10:
        return 6

def get_half_day(optimal_data):
    if optimal_data[0] %2 == 0:
        return "Chiều"
    if optimal_data[0] %2 == 1:
        return "Sáng"
    
def get_room_in_use(optimal_data):
    room_in_use = optimal_data[4]
    return room_in_use

# def get_periods_length_available(optimal_data_1, optimal_data_2):
#     output_class = []
#     if optimal_data_1[0] == optimal_data_2[0] and optimal_data_1[2] == optimal_data_2[2] and optimal_data_1[4] == optimal_data_2[4]:
#         periods_length = optimal_data_2[1] - optimal_data_2[1]
#         if periods_length == H_set[A_set.index(optimal_data_1[3])]:
#             output_class.append(optimal_data_1, optimal_data_2)
#             return output_class

# get_available_data = []
# for optimal_data_1 in key_list:
#     for optimal_data_2 in key_list:
#         get_available_data.append(get_periods_length_available(optimal_data_1, optimal_data_2))
        
optimal_data_day = []
for key in key_list:
     pass
expected_timetable = {'Mã lớp': A_set,
                      'Lớp tham gia': g_set,
                      'Mã_HP': credit_code_list,
                      'Tên HP': credit_name_list,
                      'Thứ': [2, 3, 4, 5, 6, 7],
                      'BĐ': [1, 1, 2, 3, 4, 5],
                      'KT': [4, 4, 5, 6, 6, 6],
                      'Kíp': ['Sáng', 'Chiều', 'Chiều', 'Sáng', 'Chiều', 'Chiều'],
                      'Sĩ số': class_population_list,
                      'Phòng': ['D7-101', 'D7-103', 'D7-203', 'D7-101', 'D7-103', 'D7-203'],
                      'Sức chứa': [1, 2, 3, 1, 2, 3]
                      }

expected_timetable = pd.DataFrame.from_dict(expected_timetable)

