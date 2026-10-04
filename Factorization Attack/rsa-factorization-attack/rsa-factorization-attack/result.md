## KẾT LUẬN

### Kết quả thực nghiệm

Qua quá trình cài đặt và chạy thực nghiệm thuật toán Trial Division
để tấn công RSA, em rút ra các kết quả sau:

**Bảng đo thời gian factor theo kích thước N:**

| Số bit của N | Số bước thử | Thời gian (μs) | Thời gian (ms) |
|--------------|-------------|----------------|----------------|
| 16 | 250 | 52 | 0.05 |
| 20 | 1,008 | 68 | 0.07 |
| 24 | 4,002 | 376 | 0.38 |
| 28 | 16,000 | 1,249 | 1.25 |
| 32 | 65,002 | 4,680 | 4.68 |
| 36 | 262,138 | 11,646 | 11.65 |
| 41 | 1,048,572 | 35,029 | 35.03 |
| 45 | 4,194,300 | 119,468 | 119.47 |
| 49 | 16,777,212 | 512,029 | 512.03 |
| 53 | 67,108,858 | 2,391,063 | 2,391.06 |
| 56 | 268,435,398 | 8,491,311 | 8,491.31 |

### Nhận xét về mối quan hệ giữa kích thước N và chi phí tấn công

**Số bước thử tăng theo O(√N)**

Khi N tăng thêm **2 bit**, số bước thử tăng gấp **~4 lần**:
- 16 bit → 250 bước
- 24 bit → 4,002 bước (×16)
- 32 bit → 65,002 bước (×260)
- 56 bit → 268,435,398 bước (×1,073,741)

**Thời gian tăng theo cấp số nhân**

Cứ **+2 bit** thì thời gian **×4 lần**, tức là:
- **+10 bit** → thời gian **×1000 lần**
- **+20 bit** → thời gian **×1,000,000 lần**

**Tài nguyên tiêu tốn tăng tương ứng**

| Yếu tố | Tăng theo |
|--------|-----------|
| Số phép chia (mod) | O(√N) |
| Số lần lặp vòng while | O(√N) |
| Thời gian CPU | O(√N) |
| Bộ nhớ | O(1) — không đổi |
| Năng lượng tiêu thụ | O(√N) |

### Ngoại suy cho RSA thực tế

Từ công thức `time ∝ 2^(bits/2)`, ta ngoại suy:

| Kích thước N | Số bước thử | Thời gian ước tính |
|--------------|-------------|-------------------|
| 56 bit | 2.7×10^8 | ~8.5 giây |
| 64 bit | 4.3×10^9 | ~2 phút |
| 80 bit | 1.1×10^12 | ~9 ngày |
| 128 bit | 1.8×10^19 | ~10^12 năm |
| 256 bit | 3.4×10^38 | ~10^31 năm |
| **512 bit** | **~10^77** | **vượt tuổi vũ trụ** |
| **1024 bit** | **~10^154** | **bất khả thi** |
| **2048 bit** | **~10^308** | **HOÀN TOÀN BẤT KHẢ THI** |

**Kết luận:** Kích thước N tăng **tuyến tính** về số bit, nhưng chi phí
tấn công tăng **theo cấp số nhân**. Đây chính là nền tảng an toàn của RSA.

