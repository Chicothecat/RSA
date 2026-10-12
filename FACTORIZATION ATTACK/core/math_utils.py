import math
import time

def find_prime_factors(n):
    """Tìm 2 nhân tử nguyên tố p và q của N kèm đo thời gian chạy."""
    start_time = time.perf_counter()
    p, q = None, None
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            p, q = i, n // i
            break
    elapsed_time = time.perf_counter() - start_time
    return p, q, elapsed_time

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        return None
    return x % phi