## KẾT LUẬN

### Kết quả đạt được

- Cài đặt thành công tấn công CCA trên RSA
- Mô phỏng decryption oracle giải mã mọi c khác c*
- Blinding: c' = c* × s^e mod n = 62444295
- Oracle trả về: m' = m* × s mod n = 24690
- Khôi phục: m* = m' × s^(-1) mod n = 12345
- Oracle không phát hiện (0 lần chặn)

### Nhận xét chính

a) Sức mạnh:
- Giải mã trong O(1), tức thời
- Không phụ thuộc kích thước n, phá được cả RSA-2048
- Không cần private key, chỉ cần public key và oracle
- Khó phát hiện vì không gửi trực tiếp c*

b) Điều kiện:
- Phải có decryption oracle
- Oracle phải ngây thơ, không kiểm tra ciphertext
- Phải có ciphertext mục tiêu c*

### Bài học bảo mật

1. Thuật toán mạnh không đồng nghĩa hệ thống an toàn.
   RSA toán học tốt, nhưng triển khai sai vẫn bị phá.

2. Implementation matters.
   Textbook RSA khác RSA-OAEP.

3. Không tin input từ bên ngoài.
   Oracle phải kiểm tra ciphertext hợp lệ.

### 4. Phòng chống

| Biện pháp | Mô tả |
|-----------|-------|
| OAEP Padding | Thêm padding ngẫu nhiên trước khi mã hóa |
| Kiểm tra ciphertext | Oracle từ chối ciphertext không hợp lệ |
| Giới hạn truy vấn | Chỉ cho giải mã số lần nhất định |
| RSA-KEM | Dùng RSA trao đổi khóa, không mã hóa trực tiếp |

