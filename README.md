#  RSA & Cryptographic Attacks Demonstration Suite

Hướng dẫn chạy thử demo:

Clone git về
___
git clone https://github.com/Chicothecat/RSA.git
____
cd RSA
___


Các branch trong git bao gồm



Tài liệu và mã nguồn thực hành mô phỏng các phương thức tấn công kinh điển trong hệ mật mã RSA, bao gồm giao diện tương tác trực quan (Tkinter GUI), biểu đồ thống kê (Matplotlib) và phân tích luồng dữ liệu (Attack Pipeline).

---

##  1. Tổng quan cơ bản về Hệ mật mã RSA

Trước khi phân tích các kiểu tấn công, ta cần hiểu quy trình vận hành tiêu chuẩn của RSA:

1. **Sinh khóa:**
   * Chọn 2 số nguyên tố bí mật $p$ và $q$.
   * Tính Modulus công khai: $N = p \times q$.
   * Tính hàm số Euler: $\Phi(N) = (p - 1) \times (q - 1)$.
   * Chọn số mũ công khai $e$ thỏa mãn $\gcd(e, \Phi(N)) = 1$ (thường chọn $e = 65537$ hoặc $17$).
   * Tính số mũ bí mật $d$ thỏa mãn: $d \times e \equiv 1 \pmod{\Phi(N)}$ (nghịch đảo modulo của $e$).
2. **Cặp khóa:**
   * **Khóa công khai (Public Key):** $(N, e)$ – công khai cho mọi người để mã hóa.
   * **Khóa bí mật (Private Key):** $d$ – chỉ người nhận giữ để giải mã.
3. **Mã hóa & Giải mã:**
   * **Bản rõ (Plaintext):** $m$
   * **Bản mã (Ciphertext):** $c \equiv m^e \pmod N$
   * **Giải mã:** $m \equiv c^d \pmod N$

---

##  2. Danh mục các phương thức tấn công

###  Module 1: Factorization Attack (Tấn công phân tích nhân tử)

* **Ý tưởng cốt lõi:**
  * Độ an toàn của RSA phụ thuộc trực tiếp vào độ khó của bài toán phân tích số nguyên lớn.
  * Kẻ tấn công chỉ biết cặp khóa công khai $(N, e)$. Nếu kẻ tấn công có thể tách được $N$ ngược lại thành $p$ và $q$, kẻ đó sẽ tính được $\Phi(N)$ và ngay lập tức suy ra khóa bí mật $d$.
  * Trong thực tế, nếu chọn $N$ quá nhỏ (dưới 2048-bit), kẻ tấn công hoàn toàn có thể dùng thuật toán chia thử nghiệm (*Trial Division*) để giải mã trong thời gian ngắn.

* **Pipeline luồng tấn công:**
  ```text
  [Public Key: N, e]
         │
         ▼
  [Bước 1: Tìm thừa số nguyên tố]
    - Duyệt i từ 2 đến căn bậc hai của N
    - Nếu N % i == 0 -> p = i, q = N / i
         │
         ▼
  [Bước 2: Tính hàm Euler]
    - Φ(N) = (p - 1) * (q - 1)
         │
         ▼
  [Bước 3: Khôi phục Private Key d]
    - Tính nghịch đảo modulo: d ≡ e⁻¹ mod Φ(N)
         │
         ▼
  [KẾT QUẢ: Khóa bí mật d bị lộ hoàn toàn]
'''
###  Module 2: Chosen-Ciphertext Attack - CCA (Tấn công bản mã được chọn)

* **Ý tưởng cốt lõi:**
  * Kẻ tấn công chặn được bản mã mục tiêu $c^*$ (được mã hóa từ bản rõ bí mật $m^*$), muốn đọc nội dung $m^*$ nhưng **hoàn toàn không có khóa bí mật $d$**.
  * Hệ thống giải mã (Decryption Oracle) từ chối giải mã trực tiếp nếu nhận đúng bản mã $c^*$ (để bảo vệ dữ liệu nhạy cảm).
  * **Khai thác lỗ hổng:** RSA nguyên bản (*Textbook RSA*) có tính đồng cấu nhân:
    $$(m_1 \times m_2)^e \equiv m_1^e \times m_2^e \pmod n$$
  * Kẻ tấn công sử dụng kỹ thuật làm mù (*Blinding*): nhân $c^*$ với một số ngẫu nhiên $s^e \pmod n$ để tạo ra bản mã ngụy trang $c'$. Vì $c' \neq c^*$, Oracle đồng ý giải mã và trả về $m'$. Sau đó, kẻ tấn công thực hiện gỡ mù (*Unblinding*) để thu lại nguyên vẹn thông điệp gốc $m^*$.

* **Pipeline luồng tấn công:**
  ```text
  [Bản mã mục tiêu: c*] (c* = (m*)^e mod n)
         │
         ▼
  [Bước 1: Làm mù (Blinding)]
    - Chọn số ngẫu nhiên s sao cho gcd(s, n) = 1
    - Tính: c' = (c* * s^e) mod n
         │
         ▼
  [Bước 2: Gửi Decryption Oracle]
    - Oracle giải mã c': m' = (c')^d mod n
    - Theo tính chất đồng cấu: m' = (m* * s) mod n
         │
         ▼
  [Bước 3: Gỡ mù (Unblinding)]
    - Attacker tính nghịch đảo modulo: s⁻¹ mod n
    - Khôi phục: m* = (m' * s⁻¹) mod n
         │
         ▼
  [KẾT QUẢ: Đọc được bản rõ gốc m* mà không cần biết khóa d]
'''
###  Module 3: Timing Attack (Tấn công kênh phụ qua thời gian)

* **Khái niệm & Nguyên lý:**
  * Đây là phương thức tấn công kênh phụ (*Side-Channel Attack*): không tập trung bẻ gãy cấu trúc toán học phức tạp của thuật toán mà khai thác **thời gian phản hồi thực tế của CPU/hệ thống** trong quá trình tính toán.
  * Nếu hệ thống kiểm tra mật khẩu, mã PIN hoặc chuỗi khóa bí mật sử dụng cơ chế so khớp thoát sớm (*Early-Exit Comparison*):
    * Khi kiểm tra ký tự đầu tiên bị sai $\rightarrow$ Hàm lập tức ngắt vòng lặp và trả về kết quả lỗi ngay (thời gian xử lý là $T_0$).
    * Khi ký tự đầu tiên đúng, ký tự thứ hai sai $\rightarrow$ Hệ thống phải thực hiện thêm một chu kỳ so sánh nữa rồi mới ngắt (thời gian xử lý là $T_0 + \Delta t$).
    * Càng nhiều ký tự liên tiếp từ trái qua phải khớp chính xác $\rightarrow$ Thời gian phản hồi tổng thể càng kéo dài ($T_0 + k \cdot \Delta t$).
  * Kẻ tấn công sẽ thử lần lượt từng ký tự khả dĩ ($0 \rightarrow 9$ hoặc bảng chữ cái). Ký tự nào khiến thời gian phản hồi **kéo dài nhất** chính là ký tự đúng tại vị trí đó.

* **Pipeline luồng tấn công chi tiết:**
  ```text
  [Mục tiêu: Dò chuỗi bí mật (Secret Key / PIN / Password)]
                         │
                         ▼
  ┌────────────────────────────────────────────────────────┐
  │ BƯỚC 1: Đo Baseline với input sai hoàn toàn            │
  │  - Gửi input rác (ví dụ: "xxxx")                       │
  │  - Xác định mốc thời gian nền ban đầu T_base           │
  └─────────────────────────┬──────────────────────────────┘
                            │
                            ▼
  ┌────────────────────────────────────────────────────────┐
  │ BƯỚC 2: Dò từng vị trí (Ký tự / Bit)                   │
  │  - Với vị trí pos, thử lần lượt c ∈ {'0'...'9'}        │
  │  - Tạo ứng viên: [chuỗi_đúng_đã_tìm] + c + [đệm]       │
  │  - Đo thời gian phản hồi nhiều lần (N mẫu)             │
  │  - Tính thời gian trung bình để lọc nhiễu hệ điều hành │
  │  - Ký tự có thời gian trung bình LÂU NHẤT là ký tự đúng│
  │  - Cập nhật: chuỗi_đúng_đã_tìm += c                    │
  └─────────────────────────┬──────────────────────────────┘
                            │
                            ▼
  ┌────────────────────────────────────────────────────────┐
  │ BƯỚC 3: Lặp lại đến khi hoàn tất chuỗi                 │
  │  - Tiếp tục quét cho đến khi đạt đủ độ dài bí mật      │
  └─────────────────────────┬──────────────────────────────┘
                            │
                            ▼
      [KẾT QUẢ: Khôi phục toàn vẹn 100% chuỗi bí mật]
