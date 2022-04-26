# Mô hình hỗ trợ lập thời khóa biểu cho nhóm ngành quốc tế trường đại học Bách Khoa Hà Nội

Viết chương trình xây dựng thời khóa biểu dự kiến từ dữ kiện lớp mở của từng kì và danh sách phòng cho trước

## Mô tả khái quát
Mục tiêu của mô hình là xây dựng thời khóa biểu từ danh sách lớp mở và danh sách phòng học sao cho số phòng phải sử dụng nhỏ nhất có thể.

#### Mục đích ban đầu:
- Mục đích ban đầu của mô hình là sắp xếp **thời gian** và **phòng học** cho các mã lớp học theo từng tuần cụ thể và sau đó là ghép các tuần lại để được thời khóa biểu sau cùng.
- Mô hình sẽ tìm kiếm phương án tốt nhất trong tập các phương án chấp nhận được. Tiêu chí để đánh giá là các ràng buộc và hàm mục tiêu.
#### Các yếu tố ảnh hưởng tới mô hình
- Các lớp có lịch học thất thường: Chỉ mở nửa kì, học trong một số tuần nhất định,...
- Các lớp ghép: Việc ghép lớp dựa trên mã học phần chung giữa các lớp theo chương trình đào tạo. Quy mô các lớp gồm từ 2 tới 4 lớp con ghép lại với nhau.
### Các yêu cầu đối với mô hình
Các ràng buộc chặt và ràng buộc mềm trong xây dựng mô hình
#### Yêu cầu bắt buộc
- Giờ học các lớp không bị xung đột, các khung giờ sử dụng mỗi phòng học không bị chồng chéo.
- Tất cả các lớp trong danh sách lớp mở phải được sắp xếp, giờ học của các lớp bắt đầu và kết thúc cùng  buổi.
- **Ưu tiên xếp các lớp ghép** trước rồi mới đến các lớp đơn.
- Ưu tiên sử dụng phòng trong danh sách học (trong file dữ liệu đầu vào), trong trường hợp không sắp xếp được thì có thể mượn các phòng khác ngoài danh sách.
### Xây dựng mô hình
Mô hình dự kiến được xây dựng theo các bước khái quát sau:
#### Nhập dữ liệu từ file Excel, gồm danh sách phòng học, sức chứa của phòng, 

## Giao diện người dùng của phần mềm dự kiến
![image](https://user-images.githubusercontent.com/93395558/165361324-21aa6969-1b86-4acf-9971-4ea072a1095e.png)
