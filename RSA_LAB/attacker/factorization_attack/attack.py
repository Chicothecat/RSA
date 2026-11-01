import sys,time,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from common import *
def main():
    pub=read('public_key.json');n,e=pub['n'],pub['e'];c=read('challenge.json')['ciphertext'];start=time.perf_counter()
    print(f'ATTACKER chỉ biết n={n}, e={e}, c={c}')
    print('Thử chia các ứng viên từ 2 đến căn n. n lớn có thể chạy rất lâu.')
    factor_start=time.perf_counter();p=None
    for candidate in range(2,math.isqrt(n)+1):
        remainder=n%candidate
        print(f'{n} mod {candidate} = {remainder}')
        if remainder==0:p=candidate;break
    factor_seconds=time.perf_counter()-factor_start
    if p is None:raise SystemExit('Không tìm thấy thừa số')
    q=n//p;phi=(p-1)*(q-1)
    print(f'p={p}; q=n/p={q}; phi=(p-1)(q-1)={phi}')
    d=inverse(e,phi);m=pow(c,d,n)
    print(f'd={d}; m=c^d mod n={c}^{d} mod {n}={m}')
    print(f'Thời gian tìm thừa số (gồm in từng phép chia): {factor_seconds:.6f} giây')
    save_result('factorization',dict(p=p,q=q,recovered_d=d,recovered_message=m,factor_seconds=factor_seconds),start)
if __name__=='__main__':main()
