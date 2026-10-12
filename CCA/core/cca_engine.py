import random

def extended_gcd(a, b):
    """Thuật toán Euclid mở rộng tìm GCD và hệ số nghịch đảo."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    """Tính a^(-1) mod m."""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None
    return x % m

class DecryptionOracle:
    """Mô phỏng hệ thống giải mã (nắm giữ private key d)."""
    def __init__(self, d, n, forbidden_c):
        self.d = d
        self.n = n
        self.forbidden_c = forbidden_c  # Oracle từ chối giải mã chính xác c*

    def decrypt(self, c):
        if c == self.forbidden_c:
            raise ValueError("Bị từ chối: Oracle không giải mã trực tiếp ciphertext mục tiêu c*!")
        # Trả về kết quả giải mã: c^d mod n
        return pow(c, self.d, self.n)

def execute_cca(n, e, c_star, oracle):
    """
    Thực thi quy trình CCA:
    - Bước 1: Chọn s ngẫu nhiên và tính c' = c* * s^e mod n
    - Bước 2: Nhờ Oracle giải mã c' -> m'
    - Bước 3: Tính s^(-1) mod n và khôi phục m* = m' * s^(-1) mod n
    """
    # Bước 1: Chọn s ngẫu nhiên sao cho gcd(s, n) == 1
    while True:
        s = random.randint(2, n - 1)
        gcd, _, _ = extended_gcd(s, n)
        if gcd == 1:
            break

    s_e = pow(s, e, n)
    c_prime = (c_star * s_e) % n

    # Bước 2: Gửi c_prime cho Oracle
    m_prime = oracle.decrypt(c_prime)

    # Bước 3: Gỡ mù (Unblinding)
    s_inv = mod_inverse(s, n)
    if s_inv is None:
        raise ValueError("Không thể tìm nghịch đảo modulo của s!")

    recovered_m = (m_prime * s_inv) % n

    return {
        "s": s,
        "s_e": s_e,
        "c_prime": c_prime,
        "m_prime": m_prime,
        "s_inv": s_inv,
        "recovered_m": recovered_m
    }