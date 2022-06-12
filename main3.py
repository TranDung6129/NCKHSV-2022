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
for class_group in G_set:
    test_list.append(information.get_class_code_each_class_group(class_group))

# dict_1
def get_dict_1():
    group_class_list = []
    for class_code in A_set:
        group_class_list.append(information.get_participant_class(class_code))
    # Dictionary, key là mã lớp, value là nhóm các lớp con tham gia vào mã lớp đó
    dict_1 = {}
    for class_code in A_set:
        for group_class in group_class_list:
            dict_1[class_code] = group_class
            group_class_list.remove(group_class)
            break
    return dict_1
# dict_2
def get_dict_2():
    group_class_list = []
    class_code_list = A_set
    for class_code in A_set:
        group_class_list.append(information.get_class_group(class_code))
    # Dictionary, key là mã lớp, value là nhóm các lớp con tham gia vào mã lớp đó
    dict_1 = {}
    for group_class in group_class_list:
        for class_code in class_code_list:
            if class_code not in dict_1[group_class]:
                dict_1[group_class].append(class_code)
            # class_code_list.remove(class_code)
            break
    
    return dict_1
    
