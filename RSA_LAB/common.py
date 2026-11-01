import json, math, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'
def read(name):
    p=DATA/name
    if not p.exists(): raise SystemExit('Chưa có '+str(p)+'. Hãy chạy python create_key/create_keys.py trước.')
    return json.loads(p.read_text(encoding='utf-8'))
def write(name,value):
    DATA.mkdir(exist_ok=True);(DATA/name).write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8')
def prime(n):
    return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
def inverse(a,n,verbose=True):
    r,s=n,a;x,y=0,1
    while s:
        q=r//s
        if verbose: print(f'{r} = {q} × {s} + {r%s}')
        r,s=s,r-q*s;x,y=y,x-q*y
    if r!=1: raise ValueError('Không có nghịch đảo')
    if verbose: print(f'1 = ({x}) × {a} + ({(1-x*a)//n}) × {n}; nghịch đảo = {x%n}')
    return x%n
def save_result(folder,result,start):
    elapsed=time.perf_counter()-start
    result['elapsed_seconds']=elapsed
    out=ROOT/'results';out.mkdir(exist_ok=True)
    (out/(folder+'.json')).write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(f'Thời gian toàn bộ tấn công (gồm cả in/log): {elapsed:.6f} giây')
    return elapsed
if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
