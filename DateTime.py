import pandas as pd
import numpy as np


THOI_GIAN_HOC = [{'bắt đầu': '6h45', 'kết thúc': '7h30'},
                 {'bắt đầu': '7h30', 'kết thúc': '8h15'},
                 {'bắt đầu': '8h25', 'kết thúc': '9h10'},
                 {'bắt đầu': '9h20', 'kết thúc': '10h05'},
                 {'bắt đầu': '10h15', 'kết thúc': '11h00'},
                 {'bắt đầu': '11h00', 'kết thúc': '11h45'},
                 {'bắt đầu': '12h30', 'kết thúc': '13h15'},
                 {'bắt đầu': '13h15', 'kết thúc': '14h00'},
                 {'bắt đầu': '14h10', 'kết thúc': '14h55'},
                 {'bắt đầu': '15h05', 'kết thúc': '15h50'},
                 {'bắt đầu': '16h00', 'kết thúc': '16h45'},
                 {'bắt đầu': '16h45', 'kết thúc': '17h30'},
                 {'bắt đầu': '17h45', 'kết thúc': '18h30'},
                 {'bắt đầu': '18h30', 'kết thúc': '19h15'},
                 {'bắt đầu': '19h25', 'kết thúc': '20h10'}]
class date_and_time():
    """Add date and time information"""

    def __init__(self, ma_hp, lop_con, tong_so_lop):
        self.ma_hp = ma_hp
        self.lop_con = lop_con
        self.tong_so_lop = tong_so_lop

    def kip_hoc():
        """Điền tiết bắt đầu và tiết kết thúc (điền trực tiếp vào Dataframe), sau đó sẽ tự động điền thông tin còn lại
        dựa trên thời gian bắt đầu và kết thúc như thời gian, kíp học, buổi học."""
        tiet_bat_dau = input("Lựa chọn tiết học bắt đầu: ")
        tiet_ket_thuc = input("Lựa chọn tiết học kết thúc: ")
        if tiet_bat_dau > 6:
            bat_dau = int(tiet_bat_dau) // 6
        if tiet_ket_thuc > 6:
            ket_thuc = int(tiet_ket_thuc) // 6

        pass

    def hoc_phan(ma_hoc_phan):
        pass







