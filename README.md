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

## Các yêu cầu đối với mô hình
Các ràng buộc chặt và ràng buộc mềm trong xây dựng mô hình


#### Yêu cầu bắt buộc
- Giờ học các lớp không bị xung đột, các khung giờ sử dụng mỗi phòng học không bị chồng chéo.
- Tất cả các lớp trong danh sách lớp mở phải được sắp xếp, giờ học của các lớp bắt đầu và kết thúc cùng  buổi.
- **Ưu tiên xếp các lớp ghép** trước rồi mới đến các lớp đơn.
- Ưu tiên sử dụng phòng trong danh sách học (trong file dữ liệu đầu vào), trong trường hợp không sắp xếp được thì có thể mượn các phòng khác ngoài danh sách.

## Các bước chính   

![image](https://user-images.githubusercontent.com/93395558/165380870-0a063fa1-aa65-438d-bfb8-f6cf7d61120c.png)
## Xây dựng mô hình

Mô hình dự kiến được xây dựng theo các bước khái quát sau:
### Lấy dữ liệu từ file Excel, gồm danh sách phòng học, sức chứa của phòng, kế hoạch mở lớp.

#### Lấy dữ liệu phòng học, sức chứa của phòng
- Với dữ liệu có trong sheet Biểu đồ (S), lấy các cột Số phòng mới và Số chỗ, xử lý bằng Python để có đầu ra là Dataframe chứa hai cột duy nhất là phòng học và sức chứa của phòng.

#### Lấy dữ liệu về lớp mở trong kỳ học 
- Với dữ liệu trong sheet Báo dạy, lấy những dữ liệu: tên viện sẽ dạy, tên và mã học phần, khối lượng học phần, số SV trong một lớp, số SV học lại, Ngôn ngữ dạy, Ghi chú, tổng số lớp của một mã học phần.

### Đưa dữ liệu vào mô hình
Giả sử bài toán có m lớp theo chương trình đào tạo cần xếp TKB, với n mã lớp trong học kỳ, p phòng có thể tổ chức giảng dạy.
- m lớp theo chương trình đào tạo, mỗi lớp có tên được ghi trong sheet 'Báo dạy'.
- n mã lớp học trong một kỳ sẽ bao gồm thông tin cũng được ghi trong sheet 'Báo dạy'.
- Thời khóa biểu sẽ **được xếp cho từng tuần**.

#### Thiết lập các ma trận để lưu thông tin lấy được từ dữ liệu ban đầu



### Xử lý bằng phương pháp tìm kiếm và thuật toán tìm kiếm để tìm ra phương án chấp nhận được


## Các file sẽ sử dụng bao gồm


