# Chương trình hỗ trợ lập thời khóa biểu cho nhóm ngành quốc tế đại học Bách Khoa Hà Nội
Chương trình đưa ra thời khóa biểu dự kiến cho mỗi kỳ học thông qua việc đưa vào các file dữ liệu về phòng học và các lớp mở trong kỳ.

## Các bước thực hiện
### 1. Nhập file dữ liệu đầu vào, bao gồm sheet "Báo dạy" và sheet "Danh sách phòng".
- Trong đó, sheet báo dạy sẽ chứa các thông tin về tên học phần, các lớp tham gia mã học phần đó, khối lượng tín chỉ,...
- Sheet danh sách phòng sẽ chứa tên các phòng khả dụng và sức chứa của từng phòng đó.

### 2. Xử lý file dữ liệu đầu vào để lấy các thông tin cần thiết dựa trên mô hình được đưa ra
![image](https://user-images.githubusercontent.com/93395558/170810876-4c9355f0-7c72-44b8-a293-1809cf0eb54a.png)

- Trong đó thì file 'classroom.py' sẽ trích xuất dữ liệu về lớp học, file 'information.py' sẽ trích xuất các thông tin còn lại.

### 3. Chuyển từ mô hình toán học thành code

- Với mô hình đã được xây dựng, nhập các biến, ràng buộc và hàm mục tiêu vào chương trình.
- Được thực hiện trong file 'problem_modelling.py'.

### 4.Tối ưu hóa mô hình
- Thực hiện tối ưu hóa mô hình được cung cấp bằng các gói Solver có sẵn là 'gurobipy' và 'cplex'.
- Bước này sẽ được thực hiện trực tiếp trong file 'main.py'.

### 5. Tạo ra một Dataframe mới chứa các dữ liệu đã được tối ưu
- Qua việc tối ưu mô hình sẽ cho ra các dữ liệu mới đã được tối ưu theo đúng yêu cầu về đầu ra của mô hình.
- Dataframe này sẽ được xây dựng trong file 'timetable_ouput'.

### 6. Xuất ra Dataframe đã tạo 
- Xuất ra file Excel Dataframe đã được tạo 

### 7. Xây dựng giao diện người dùng
- Sử dụng gói Tkinter để thiết kế giao diện người dùng cho phần mềm về sau.

# Ý kiến bổ sung về mô hình
- Nên đưa ra một bộ quy tắc cho file Excel về sau, như việc nó sẽ bao gồm các sheet nào, mỗi sheet có format ra sao để có thể dễ dàng hơn trong việc xử lý dữ liệu.
