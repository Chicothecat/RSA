

<img width="122" height="692" alt="FAT" src="https://github.com/user-attachments/assets/72e698aa-7f8b-44cf-a29d-c39df0f08bd9" />

## FACTORIZATION ATTACK TRÊN RSA

### Nguyên lý

RSA bảo mật dựa vào **bài toán phân tích thừa số nguyên tố**:

- **Chiều xuôi:** Có `p, q` → tính `n = p × q`
- **Chiều ngược:** Có `n` → tìm `p, q`

→ Nếu tìm được `p, q` từ `n`, RSA bị phá hoàn toàn.

### Quy trình tấn công

**Input:** Public key `(n, e)` và ciphertext `c`

**Các bước:**

1. **Thu thập:** Lấy `n, e` từ public key
2. **Factor n:** Tìm `p, q` sao cho `p × q = n`
3. **Tính φ(n):** `φ(n) = (p - 1)(q - 1)`
4. **Tính d:** `d = e^(-1) mod φ(n)`
5. **Khai thác:**
   - Giải mã: `m = c^d mod n`
   - Giả mạo chữ ký: `σ = H(m)^d mod n`

### Cài đặt

**Cấu trúc code:**

| File | Chức năng |
|------|-----------|
| `rsa_demo.cpp` | Tạo RSA key + mã hóa |
| `factorization.cpp` | Tấn công factor `n` |
| `benchmark.cpp` | Đo thời gian theo kích thước N |

**Thuật toán Trial Division:**

```cpp
for i = 2 to √n:
    if n mod i == 0:
        p = i
        q = n / i
        return (p, q)
