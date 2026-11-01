import hashlib,time
from common import read
# Oracle giữ bí mật. Đây là ranh giới logic của lab, không phải sandbox bảo mật.
class CCAOracle:
    def __init__(self):
        self._key=read('private_key.json');self._target=read('challenge.json')['ciphertext'];self.calls=0
    def decrypt(self,c):
        if c==self._target:raise ValueError('Oracle từ chối bản mã mục tiêu')
        if not 0<=c<self._key['n']:raise ValueError('Bản mã ngoài miền')
        self.calls+=1
        return pow(c,self._key['d'],self._key['n'])
def leakage(c,index,state):
    # Mô hình chi phí cố ý: 0..3 đơn vị, dự đoán được nếu đoán đúng trạng thái.
    return hashlib.blake2s(f'{c}:{index}:{state}'.encode(),digest_size=1).digest()[0]&3
class TimingOracle:
    def __init__(self,unit_seconds=0.00008):
        self._key=read('private_key.json');self.width=self._key['n'].bit_length();self.unit=unit_seconds;self.calls=0
    def query(self,c):
        # Không trả plaintext, bit, state hoặc d. Chỉ thời gian đo perf_counter.
        n=self._key['n'];state=1;start=time.perf_counter()
        for i,bit in enumerate(format(self._key['d'],f'0{self.width}b')):
            state=state*state%n
            if bit=='1':state=state*c%n
            cost=leakage(c,i,state)*self.unit
            end=time.perf_counter()+cost
            while time.perf_counter()<end:pass
        self.calls+=1
        return time.perf_counter()-start
