## TIMING ATTACK

### Nguyên lý

Timing Attack là tấn công kênh phụ, khai thác thời gian
thực thi của thuật toán để suy ra thông tin bí mật.

Nguyên tắc: nếu thời gian chạy phụ thuộc vào dữ liệu bí mật, attacker
đo thời gian để suy ra dữ liệu đó.

### Điều kiện

- Đo được thời gian phản hồi của hệ thống
- Thời gian thực thi phụ thuộc vào dữ liệu bí mật
- Gửi được nhiều truy vấn để lấy mẫu thống kê

### Cơ chế

Thời gian thực thi khác nhau khi thuật toán xử lý các nhánh khác nhau.
Sự khác biệt này rò rỉ thông tin về dữ liệu bí mật.

### Quy trình

    BƯỚC 1: Đo baseline với input sai hoàn toàn

    BƯỚC 2: Dò từng đơn vị thông tin (ký tự, bit)
        Với mỗi vị trí, thử mọi khả năng
        Đo thời gian phản hồi
        Khả năng cho thời gian lâu nhất là đúng

    BƯỚC 3: Lặp đến khi tìm hết bí mật

    BƯỚC 4: Đo nhiều lần, lấy trung bình để lọc nhiễu


Phòng chống: viết code constant-time, dùng blinding, không thoát sớm.
