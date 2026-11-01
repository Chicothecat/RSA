# RSA LAB Python - Bob tạo khóa trước rồi đối thủ tấn công

## Chạy trên Windows

Giải nén ZIP. Mở thư mục RSA_LAB, bấm thanh địa chỉ Explorer, gõ powershell rồi Enter. Chạy:

```powershell
python run_all.py
```

Hoặc nhấp đôi RUN_DEMO.bat. Mọi đường dẫn dữ liệu tính theo vị trí file, không phụ thuộc thư mục terminal.

## Chạy từng phần

```powershell
python create_key/create_keys.py
python create_key/public_key.py
python create_key/private_key.py
python attacker/factorization_attack/attack.py
python attacker/cca/attack.py
python attacker/timing_attack/attack.py
```

Bob tạo mặc định p=61,q=53,e=17,m=65. Khóa công khai n=3233,e=17; d=2753; bản mã c=2790. public_key.py và private_key.py trình bày lại riêng hai phần từ khóa Bob đã tạo, không sinh hai cặp khóa khác nhau.

Tự chọn bộ số nhỏ:

```powershell
python create_key/create_keys.py --p 5 --q 11 --e 3 --m 12
```

## Cấu trúc và dữ liệu

- create_key/create_keys.py: in toàn bộ quá trình Bob tạo public/private key, tính d bằng Euclid mở rộng; Alice tạo bản mã mẫu.
- create_key/public_key.py: in riêng bước tạo public key.
- create_key/private_key.py: in riêng bước tạo private key.
- attacker/factorization_attack/attack.py: thử chia n, in từng phép chia, tìm p,q, tính phi,d rồi giải mã.
- attacker/cca/attack.py: chọn r, tạo c', gọi oracle Bob, dùng nghịch đảo r khôi phục m. Không khôi phục d.
- attacker/timing_attack/attack.py: thu tổng thời gian từ oracle, đoán các bit d bằng mô hình độ trễ và tìm kiếm nhiều giả thuyết.
- bob/oracles.py: giữ khóa bí mật và cung cấp hai oracle cục bộ.
- common.py: I/O, số học và lưu thời gian.
- data/public_key.json: chỉ n,e; data/challenge.json: chỉ ciphertext. Hai file này attacker được biết.
- data/private_key.json: khóa bí mật phía Bob; data/bob_expected.json: bản rõ gốc chỉ để người học kiểm tra. Các thuật toán attacker không đọc hai file này.
- results/: kết quả JSON từng cuộc tấn công, timing_measurements.csv chứa số đo thật từng đầu vào.

Oracle chạy cùng máy và cùng tiến trình nên đây là ranh giới vai trò trong mã nguồn, không phải cách ly quyền truy cập bằng hệ điều hành. Toàn bộ chương trình là lab của bạn, không có kết nối tới máy bên ngoài.

## Timing attack hoạt động thế nào

Oracle thực sự tính c^d mod n bằng bình phương và nhân. Sau mỗi bit, nó cố ý thêm độ trễ 0..3 đơn vị theo hàm băm của ciphertext, vị trí bit và trạng thái trung gian. Đây là rò rỉ nhân tạo để quan sát nguyên lý, không phải tái hiện đầy đủ timing attack Kocher hay lỗ hổng của thư viện RSA thực tế.

Attacker biết thiết kế và đơn vị độ trễ nhưng không biết d/trạng thái của Bob. Với mỗi giả thuyết prefix của d, attacker tính thử các trạng thái, dự đoán chi phí và so với tổng thời gian đo bằng perf_counter. Beam search giữ 8 giả thuyết mỗi vòng. Ở cuối, kiểm chứng khóa ứng viên bằng các phép mã hóa và giải mã với public key. Oracle không trả plaintext cho timing attacker.

Mỗi đầu vào được đo lặp rồi lấy giá trị nhỏ nhất để giảm nhiễu dương do hệ điều hành. Không có cam kết khôi phục thành công mọi lần trên mọi máy; thất bại được báo rõ, không lấy d thật để giả thành kết quả tấn công. Nếu cần:

```powershell
python attacker/timing_attack/attack.py --samples 2400 --repeats 5 --unit-us 150
```

Timing giới hạn n tối đa 20 bit để học; bộ mặc định chỉ 12 bit. Thời gian thực nghiệm tùy máy, độ trễ cố ý, lượng mẫu và nhiễu; không phản ánh thời gian phá RSA an toàn trong thực tế.

## Hiểu đúng các kết quả

Factorization: khôi phục p,q và một số mũ bí mật d hợp lệ.
CCA: khôi phục bản rõ qua oracle giải mã RSA thô; không tìm khóa. Oracle chặn c mục tiêu nhưng cho giải mã c' khác. Với c=0 không tạo được c' khác qua phép nhân, chương trình báo không thực hiện được.
Timing: cố gắng khôi phục d bằng đo thời gian trên bộ giải mã cố ý rò rỉ. Cần nhiều mẫu, không suy bit bằng quy tắc nhanh=0/chậm=1.

Các thời gian lưu JSON dùng perf_counter: tổng tấn công gồm I/O/in console, factorization có thêm thời gian thử chia, timing có riêng thu mẫu và phân tích. Không so sánh trực tiếp ba con số như một benchmark công bằng vì các giả định và tài nguyên oracle khác nhau.

Chạy lại create_keys sẽ thay bộ khóa/thông điệp hiện tại. Chạy lại một attack sẽ thay file kết quả tương ứng. Không dùng khóa nhỏ/RSA không padding của lab để bảo vệ dữ liệu thật.


## Alice gửi văn bản cho Bob

Hai thư mục mới encrypt và decrypt minh họa văn bản UTF-8, mặc định "Hello Bob".

```powershell
python create_key/create_keys.py
python encrypt/encrypt.py --text "Hello Bob"
python decrypt/decrypt.py
```

Alice nhập văn bản, mã hóa bằng public_key.json. Gói gửi data/alice_to_bob.json chỉ chứa định dạng, n,e công khai và danh sách số bản mã, không chứa văn bản hoặc byte bản rõ. Bob dùng private_key.json để giải mã, ghép byte UTF-8, hiện "Hello Bob" và lưu results/bob_received.txt. Có thể mở gói JSON trước khi chạy decrypt để xem chỉ có bản mã.

Để thấy tách biệt từng vai trò, chạy ba lệnh trên riêng. run_all chạy tự động cả Alice và Bob, nên tất nhiên hiển thị cả văn bản Alice nhập lúc đầu và nội dung Bob đọc lúc cuối. Không có cơ chế giấu nội dung Alice đã hiển thị trong lịch sử terminal.

Đây là RSA thô theo từng byte, không padding, chỉ để học: ký tự lặp tạo cùng khối và người biết public key có thể thử đủ 256 byte để tra ngược. Vì thế không được kết luận “không ai khác đọc được” đối với bản demo này. Bảo mật văn bản thật cần cơ chế như RSA-OAEP hoặc mã hóa lai RSA với AES; không dùng cách từng byte này.

n cần lớn hơn 255; bộ khóa mặc định thỏa điều kiện. Bản mã văn bản độc lập với challenge.json dùng cho ba attack cũ, nên chúng vẫn giữ ví dụ số m=65. Khóa nhỏ của project vốn cũng bị factorization phá được.
