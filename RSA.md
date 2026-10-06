# CHƯƠNG 3. CÁC BƯỚC THỰC HIỆN CỦA THUẬT TOÁN

## 3.1 Sinh khóa

Quá trình sinh khóa RSA được thiết kế sao cho việc tìm ra khóa bí mật từ khóa công khai là một bài toán khó giải quyết trong thời gian hợp lý, trừ khi người ta có được các thông tin bí mật liên quan (như các thừa số nguyên tố của modulus n).

Quá trình sinh khóa bao gồm các bước sau:

### 3.1.1 Thuật toán

#### 3.1.1.1 Chọn 2 số nguyên tố lớn p và q

- RSA bắt đầu bằng việc chọn hai số nguyên tố ngẫu nhiên và lớn, ký hiệu là p và q. Hai số này phải đủ lớn để đảm bảo tính bảo mật.
- Kích thước của p và q thường là hàng trăm, thậm chí hàng nghìn bit. Ví dụ, với một hệ thống RSA 2048 bit, mỗi số nguyên tố p và q có kích thước khoảng 1024 bit.

#### 3.1.1.2 Tính n, là tích của p và q

- Tính toán n như sau: `n = p × q`.
- Giá trị n được gọi là modulus và sẽ được sử dụng cho cả quá trình mã hóa và giải mã.

#### 3.1.1.3 Tính hàm số phi Euler ϕ(n)

- Hàm phi Euler của n, ký hiệu là ϕ(n) được tính như sau:

  `ϕ(n) = (p − 1) × (q − 1)`

- Hàm phi Euler đại diện cho số lượng các số nguyên dương nhỏ hơn n mà không có ước số chung với n.

#### 3.1.1.4 Chọn một số nguyên e

- Chọn một số nguyên e sao cho:

  `1 < e < ϕ(n)` và `gcd(e, ϕ(n)) = 1`

  (tức là e và ϕ(n) nguyên tố cùng nhau).
- Số e này sẽ là khóa công khai dùng để mã hóa. Một giá trị phổ biến của e là 65537, vì nó đủ lớn để bảo mật nhưng vẫn đảm bảo hiệu quả tính toán.

#### 3.1.1.5 Tính khóa bí mật d

- Khóa bí mật d được tính dựa trên e và ϕ(n) sao cho:

  `d × e ≡ 1 (mod ϕ(n))`

- Điều này có nghĩa là d là nghịch đảo modular của e theo ϕ(n). Để tính d, người ta thường sử dụng thuật toán Euclid mở rộng (Extended Euclidean Algorithm).

## 3.1.2 Khóa công khai và khóa bí mật

- **Khóa công khai:** Là cặp `(e, n)`. Khóa này được công khai và dùng để mã hóa các thông điệp.
- **Khóa bí mật:** Là cặp `(d, n)`. Khóa này phải được giữ bí mật và dùng để giải mã các thông điệp đã được mã hóa bằng khóa công khai tương ứng.

## 3.1.3 Một số yêu cầu với quá trình sinh khóa

Dưới đây liệt kê các yêu cầu đặt ra với các tham số sinh khóa và khóa để đảm bảo sự an toàn của cặp khóa RSA. Các yêu cầu cụ thể gồm:

### Yêu cầu với các tham số sinh khóa p và q

- Các số nguyên tố p và q phải được chọn sao cho việc phân tích n (`n = p × q`) là không khả thi về mặt tính toán. p và q nên có cùng độ lớn (tính bằng bit) và phải là các số đủ lớn. Nếu n có kích thước 2048 bit thì p và q nên có kích thước khoảng 1024 bit.
- Hiệu số p – q không nên quá nhỏ, do nếu p – q quá nhỏ, tức p ≈ q và p ≈ √n. Như vậy, có thể chọn các số nguyên tố ở gần √n và thử. Khi có được p, có thể tính q và tìm ra d là khóa bí mật từ khóa công khai e và Φ(n) = (p - 1)(q - 1). Nếu p và q được chọn ngẫu nhiên và p – q đủ lớn, khả năng hai số này bị phân tích từ n giảm đi.

### Vấn đề sử dụng số mũ mã hóa (e) nhỏ

- Khi sử dụng số mũ mã hóa (e) nhỏ, chẳng hạn e = 3 có thể tăng tốc độ mã hóa. Kẻ tấn công có thể nghe lén và lấy được bản mã, từ đó phân tích bản mã để khôi phục bản rõ.
- Do số mũ mã hóa nhỏ nên chi phí cho phân tích, hoặc vét cạn không quá lớn. Do vậy, nên sử dụng số mũ mã hóa e đủ lớn và thêm chuỗi ngẫu nhiên vào khối rõ trước khi mã hóa để giảm khả năng bị vét cạn hoặc phân tích bản mã.

### Vấn đề sử dụng số mũ giải mã (d) nhỏ

- Khi sử dụng số mũ giải mã (d) nhỏ, có thể tăng tốc độ giải mã.
- Nếu d nhỏ và gcd(p-1, q-1) cũng nhỏ thì d có thể tính được tương đối dễ dàng từ khóa công khai (n, e).
- Do vậy, để đảm bảo an toàn, nên sử dụng số mũ giải mã d đủ lớn.

## 3.1.4 Ví dụ

Dưới đây là một ví dụ đơn giản về quá trình sinh khóa RSA:

### 3.1.4.1 Chọn 2 số nguyên tố p và q

Giả sử chọn:

`p = 61` và `q = 53`

### 3.1.4.2 Tính n

`n = 61 × 53 = 3233`

### 3.1.4.3 Tính ϕ(n)

`ϕ(n) = (61 − 1) × (53 − 1) = 60 × 52 = 3120`

### 3.1.4.4 Chọn e

Giả sử chọn `e = 17`, vì:

`gcd(17, 3120) = 1`

### 3.1.4.5 Tính khóa bí mật d

- Sử dụng thuật toán Euclid mở rộng, tìm d sao cho:

  `d × 17 ≡ 1 (mod 3120)`

- Ta tính được:

  `d = 2753`

### 3.1.4.6 Kết quả

- **Khóa công khai:** `(e = 17, n = 3233)`.
- **Khóa bí mật:** `(d = 2753, n = 3233)`.

## 3.1.5 Kết luận

Thuật toán sinh khóa của RSA là bước nền tảng, đảm bảo tính an toàn và hiệu quả của phương pháp mã hóa bất đối xứng. Quá trình này dựa trên việc chọn hai số nguyên tố lớn để tạo ra các cặp khóa có tính chất toán học đặc biệt, giúp mã hóa và giải mã hoạt động một cách an toàn. Độ phức tạp trong việc phân tích thừa số của một số lớn đảm bảo rằng việc phá vỡ RSA là cực kỳ khó khăn với khả năng tính toán hiện tại. Chính vì vậy, thuật toán sinh khóa không chỉ quyết định hiệu quả mà còn đảm bảo tính bảo mật của hệ thống RSA.

## 3.2 Mã hóa (Encryption)

Quá trình mã hóa một thông điệp trong RSA sử dụng khóa công khai `(e, n)`. Giả sử M là thông điệp cần mã hóa (được chuyển đổi thành một số nguyên M sao cho M < n), quá trình mã hóa sẽ được thực hiện như sau:

`C = M^e (mod n)`

Trong đó:

- M là thông điệp gốc (plaintext).
- C là bản mã (ciphertext).

## 3.3 Giải mã (Decryption)

- Sau khi nhận được bản mã C, người nhận sử dụng khóa riêng để giải mã và khôi phục thông điệp gốc.
- Thông điệp gốc M được tính bằng cách:

  `M = C^d (mod n)`

Nhờ vào cách mà d được tính, phương trình này sẽ khôi phục chính xác thông điệp ban đầu.

## 3.4 Ví dụ tổng quan

Để kết hợp với phần sinh khóa và kết hợp mã hóa, giải mã, có một ví dụ dưới đây.

Giả sử bạn có cặp khóa RSA với các tham số:

- `p = 61`
- `q = 53`
- `n = p × q = 61 × 53 = 3233`
- `ϕ(n) = (61 − 1) × (53 − 1) = 3120`
- Chọn `e = 17` (thoả mãn `gcd(17, 3120) = 1`).
- Tính `d = 2753`, là nghịch đảo modular của e theo modulo 3120.

Khóa công khai là `(n, e) = (3233, 17)`, và khóa riêng là `(n, d) = (3233, 2753)`.

### Mã hóa

Giả sử thông điệp là `M = 65`. Bản mã C sẽ được tính như sau:

`C = 65^17 mod 3233 = 2790`

### Giải mã

Khi nhận được `C = 2790`, sử dụng khóa riêng để giải mã:

`M = 2790^2753 mod 3233 = 65`

→ Thông điệp gốc `M = 65` đã được khôi phục chính xác.

## 3.5 Chuyển đổi văn bản rõ

Các hệ thống mật mã như RSA hoạt động trên các con số, nhưng các thông điệp được tạo thành từ các ký tự. Chúng ta nên chuyển đổi các thông điệp của mình thành các con số như thế nào để có thể áp dụng các phép toán?

Cách phổ biến nhất là lấy các byte thứ tự của thông điệp, chuyển đổi chúng thành hệ thập lục phân và nối lại. Điều này có thể được hiểu là một số cơ số 16/hệ thập lục phân và cũng được biểu diễn ở hệ cơ số 10/hệ thập phân.

### Ví dụ chuyển đổi văn bản

Với đoạn message `HELLO` được tạo như bên trên, mình sẽ tiến hành giải mã ngược lại theo các bước. Hoặc mình có thể sử dụng hàm `long_to_bytes()` trong thư viện pwntools của Python để có thể xử lý một cách dễ dàng hơn.

Đoạn code Python trong hình sử dụng thư viện `Crypto.Util.number` và `pwn` để chuyển đổi một số nguyên lớn thành chuỗi ký tự dạng byte rồi giải mã thành chuỗi ký tự (string).

### Giải thích chi tiết

#### 1. Thư viện được sử dụng

- `from Crypto.Util.number import *`: Đây là một phần của thư viện PyCryptodome, cung cấp các công cụ làm việc với số lớn, như chuyển đổi giữa số nguyên và byte.
- `from pwn import *`: Đây là một phần của thư viện pwntools, được sử dụng nhiều trong lĩnh vực bảo mật và CTF để hỗ trợ các thao tác liên quan đến mã hóa, giải mã, và tương tác với hệ thống.

#### 2. Ý nghĩa các dòng lệnh

- Dòng 4: `n = 310400273487`

  Gán số nguyên lớn `310400273487` vào biến n.

- Dòng 6: `print(long_to_bytes(n).decode())`

  - `long_to_bytes(n)`: Chuyển đổi số nguyên n thành chuỗi byte. Đây là hàm thường dùng khi muốn trích xuất thông điệp được mã hóa thành số nguyên.
  - `.decode()`: Giải mã chuỗi byte thu được từ `long_to_bytes(n)` thành chuỗi ký tự (string) theo mã hóa UTF-8 (mặc định).
  - `print(...)`: In chuỗi kết quả ra màn hình.

#### 3. Kết quả

- Khi chạy đoạn mã, kết quả in ra là `HELLO`.
- Điều này có nghĩa là số nguyên `310400273487` được biểu diễn trong dạng byte là chuỗi ký tự `"HELLO"` sau khi giải mã.

### Tóm lại

Đoạn mã này sử dụng thuật toán chuyển đổi từ số nguyên lớn sang chuỗi ký tự. Đây là một kỹ thuật phổ biến trong bảo mật, thường xuất hiện trong các bài tập CTF liên quan đến RSA, nơi thông điệp được mã hóa thành số nguyên và cần phải chuyển đổi ngược lại.
