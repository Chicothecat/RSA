## CHOSEN-CIPHERTEXT ATTACK (CCA)

### Nguyên lý

**CCA** là tấn công trong đó attacker chủ động
chọn ciphertext và gửi cho hệ thống giải mã, rồi phân tích kết quả
để tìm ra plaintext hoặc private key.

**Điều kiện:**
- Attacker có quyền truy cập decryption oracle (hệ thống giải mã)
- Oracle giải mã mọi ciphertext attacker gửi vào (trừ ciphertext mục tiêu)
- Attacker không biết private key

**Mục tiêu:**
- Giải mã ciphertext mục tiêu `c*` mà không cần biết `d`
- Hoặc tìm ra plaintext `m*`

### Hai biến thể

| Loại | Mô tả |
|------|-------|
| Lunchtime CCA | Attacker tấn công trước khi có `c*` |
| Adaptive CCA | Attacker tấn công sau khi có `c*`, chọn ciphertext dựa trên kết quả trước |

### Quy trình tấn công RSA (RSA-CAA)

**Input:** 
- Public key `(n, e)`
- Ciphertext mục tiêu `c*`
- Decryption oracle `O(c) = c^d mod n`

**Procedure:**
BƯỚC 1: Blinding
Chọn s ngẫu nhiên
Tính c' = c* × s^e mod n

BƯỚC 2: Gửi oracle
m' = O(c') = (c')^d mod n
= m* × s mod n

BƯỚC 3: Khôi phục
m* = m' × s^(-1) mod n
