import sys,time,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from common import *
from bob.oracles import CCAOracle
def main():
    pub=read('public_key.json');n,e=pub['n'],pub['e'];c=read('challenge.json')['ciphertext']
    oracle=CCAOracle();start=time.perf_counter()
    print(f'ATTACKER biết n={n}, e={e}, c={c}; không biết d,p,q.')
    r=None
    for candidate in range(2,n):
        if math.gcd(candidate,n)==1 and c*pow(candidate,e,n)%n!=c:r=candidate;break
    if r is None:
        save_result('cca',{'success':False,'reason':'Không tìm được c khác c mục tiêu (ví dụ c=0).'},start);return
    print(f'Chọn r={r}; gcd(r,n)=1. Tính nghịch đảo:')
    ri=inverse(r,n);cp=c*pow(r,e,n)%n
    print(f"c'=c*r^e mod n={c}*{r}^{e} mod {n}={cp}")
    print("Vì c' ≡ (mr)^e, Bob giải mã c' sẽ cho m'=mr mod n.")
    mp=oracle.decrypt(cp)
    print(f"Oracle trả m'={mp}; KHÔNG trả khóa bí mật.")
    m=mp*ri%n
    print(f"m=m'*r^(-1) mod n={mp}*{ri} mod {n}={m}")
    save_result('cca',dict(success=True,recovered_message=m,oracle_queries=oracle.calls,recovered_private_key=False),start)
if __name__=='__main__':main()
