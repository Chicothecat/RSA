import time
import string
import statistics

# Độ trễ giả lập trên mỗi ký tự so khớp đúng (để mô phỏng trên môi trường OS thông thường)
DELAY_PER_CHAR = 0.005 

class VulnerableServer:
    """Mô phỏng hệ thống kiểm tra mật khẩu bị rò rỉ thời gian."""
    def __init__(self, secret: str):
        self.secret = secret

    def verify(self, candidate: str) -> bool:
        if len(candidate) != len(self.secret):
            return False

        for real_char, guess_char in zip(self.secret, candidate):
            if real_char != guess_char:
                return False  # THOÁT SỚM -> LÀM RÒ RỈ THỜI GIAN
            # Giả lập tải tính toán xử lý chuỗi
            time.sleep(DELAY_PER_CHAR)

        return True

def measure_average_time(server: VulnerableServer, candidate: str, samples: int = 15) -> float:
    """Bước 4: Đo nhiều lần, lấy trung bình để lọc nhiễu."""
    timings = []
    for _ in range(samples):
        t0 = time.perf_counter()
        server.verify(candidate)
        t1 = time.perf_counter()
        timings.append(t1 - t0)
    return statistics.mean(timings)