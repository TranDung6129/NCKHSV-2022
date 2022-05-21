""" Tạo một dataframe để chứa các dữ liệu thêm vào """

import numpy as np
import pandas as pd
import os

expected_timetable = {'Mã lớp': 'VD: 123456',
                      'Mã lớp kèm': 'VD: 123456',
                      'Mã_HP': 'VD: IT4060Q',
                      'Tên_HP': 'VD: Lập trình mạng',
                      'Khối lượng': 'VD: 2(2-1-0-4)',
                      'Ghi chú': 'VD: [SIE-66-Tiếng Anh]-IT-LTU-K64C',
                      # Các cột với thời gian cố định thì khi làm chương trình sẽ tạo ra một hàm lựa chọn
                      'Buổi': 'VD: 1',
                      'Thứ': 'VD: 2',
                      'Thời_gian': 'VD: 1230-1455',
                      # Khi chọn khoảng thời gian bắt đầu và kết thúc sẽ tự động điền tiết bắt đầu và tiét kết thúc
                      'BĐ': 'VD: 1',
                      'KT': 'VD: 3',
                      # Kíp sẽ tự động được đặt là sáng hoặc chiều dựa vào tiết kết thúc (do phải kết thúc trong cùng
                      # một buổi)
                      'Kíp': 'VD: Chiều',
                      # Tuần sẽ được thêm sau bước chọn được phương án chấp nhận được?
                      'Tuần': 'VD: 27-34,36-43',
                      'Phòng': 'VD: D7-105',
                      # SLĐK phải nhỏ hơn số lượng max
                      'SlĐK': 'VD: 88',
                      'Hủy': False,
                      'Trạng thái': 'Điều chỉnh ĐK',
                      # Có ba loại lớp là LT, BT, LT+BT
                      'Loại lớp': 'VD: LT',
                      # Có thể có ba đợt mở lớp, đợt A, đợt B, đợt AB
                      'Đợt mở': 'AB',
                      'Mã_QL': 'SIE',
                      }

expected_timetable = pd.DataFrame(expected_timetable, index=[0])
print(expected_timetable)
