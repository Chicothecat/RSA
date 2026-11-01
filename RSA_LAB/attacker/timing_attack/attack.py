import sys,time,random,argparse,math,statistics,csv
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from common import *
from bob.oracles import TimingOracle,leakage
def mse_fit(predicted,measured):
    # Offset tự do hấp thụ thời gian nền; unit đã biết từ thiết kế lab.
    residual=[t-p for p,t in zip(predicted,measured)]
    mean=statistics.mean(residual)
    return sum((v-mean)**2 for v in residual)/len(residual)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--samples',type=int,default=1200);parser.add_argument('--repeats',type=int,default=3);parser.add_argument('--unit-us',type=float,default=80)
    a=parser.parse_args()
    if a.samples<64 or a.repeats<1 or a.unit_us<=0:parser.error('samples>=64, repeats>=1, unit-us>0')
    pub=read('public_key.json');n,e=pub['n'],pub['e'];c=read('challenge.json')['ciphertext']
    oracle=TimingOracle(a.unit_us/1e6)
    if oracle.width>20:parser.error('Lab timing chỉ dùng n <=20 bit. Hãy tạo lại khóa mặc định.')
    start=time.perf_counter();rng=random.Random(2026)
    inputs=[rng.randrange(2,n-1) for _ in range(a.samples)]
    print('TIMING ATTACK trên RSA cố ý có độ trễ phụ thuộc trạng thái trung gian.')
    print('Không đọc private_key trong attacker. Oracle chỉ trả tổng thời gian, không trả bản rõ.')
    print(f'Biết từ thiết kế: số vòng={oracle.width}, đơn vị độ trễ={a.unit_us} micro giây.')
    print('Đo wall-clock bằng perf_counter; không dùng thời gian mô phỏng thay số đo.')
    measurements=[];measure_start=time.perf_counter()
    for i,x in enumerate(inputs):
        measurements.append(min(oracle.query(x) for _ in range(a.repeats)))
        if (i+1)%200==0:print(f'Đã đo {i+1}/{len(inputs)} đầu vào')
    measure_seconds=time.perf_counter()-measure_start
    out=ROOT/'results';out.mkdir(exist_ok=True)
    with (out/'timing_measurements.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['ciphertext','seconds']);w.writerows(zip(inputs,measurements))
    # Beam search giữ 8 giả thuyết: tránh một quyết định sai làm hỏng toàn bộ prefix.
    beam=[('',[1]*len(inputs),[0.0]*len(inputs))]
    analysis_start=time.perf_counter()
    for index in range(oracle.width):
        candidates=[]
        for prefix,states,costs in beam:
            for bit in (0,1):
                new_states=[(s*s%n)* (x if bit else 1)%n for s,x in zip(states,inputs)]
                new_costs=[v+leakage(x,index,s)*oracle.unit for v,x,s in zip(costs,inputs,new_states)]
                score=mse_fit(new_costs,measurements)
                candidates.append((score,prefix+str(bit),new_states,new_costs))
        candidates.sort(key=lambda v:v[0]);beam=[(p,s,t) for _,p,s,t in candidates[:8]]
        print(f'Bit {index+1}: tốt nhất prefix={candidates[0][1]}, sai số={candidates[0][0]:.3e}; giữ {len(beam)} giả thuyết')
    # Kiểm chứng ứng viên bằng quan hệ RSA công khai, không dùng d thật.
    recovered=None
    for prefix,_,_ in beam:
        guess=int(prefix,2)
        if guess and all(pow(pow(x,e,n),guess,n)==x for x in (0,1,2,3,7,n-1) if x<n):
            recovered=guess;break
    analysis_seconds=time.perf_counter()-analysis_start
    success=recovered is not None
    result=dict(success=success,recovered_d=recovered,oracle_queries=oracle.calls,samples=len(inputs),measurement_seconds=measure_seconds,analysis_seconds=analysis_seconds,artificial_leakage=True)
    if success:
        m=pow(c,recovered,n);result['recovered_message']=m
        print(f'Khôi phục ứng viên d={recovered}; kiểm chứng qua public key thành công; m=c^d mod n={m}')
    else:print('CHƯA KHÔI PHỤC ĐƯỢC KHÓA. Không thay bằng khóa thật. Hãy tăng --samples, --repeats hoặc --unit-us.')
    print(f'Thời gian thu mẫu: {measure_seconds:.6f}s; phân tích: {analysis_seconds:.6f}s')
    save_result('timing',result,start)
    return 0 if success else 1
if __name__=='__main__':sys.exit(main())
