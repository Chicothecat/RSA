import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *

def decrypt_text(blocks,n,d):
    if not isinstance(blocks,list) or any(type(c) is not int or not 0<=c<n for c in blocks):
        raise ValueError('Các khối bản mã phải là số nguyên trong 0..n-1')
    decoded=[pow(c,d,n) for c in blocks]
    if any(b>255 for b in decoded):raise ValueError('Giải mã không ra byte hợp lệ; có thể sai khóa hoặc gói đã bị sửa')
    return bytes(decoded).decode('utf-8'),decoded

def main():
    packet=read('alice_to_bob.json');key=read('private_key.json')
    if packet.get('format')!='textbook-rsa-utf8-byte-v1':raise SystemExit('Định dạng gói không hỗ trợ')
    if packet.get('n')!=key['n']:raise SystemExit('Gói không khớp khóa Bob. Hãy mã hóa lại sau khi đổi khóa.')
    blocks=packet['ciphertext_blocks']
    print('BOB — NHẬN GÓI BẢN MÃ')
    print(blocks)
    print(f"Dùng PRIVATE KEY Bob: n={key['n']}, d={key['d']}")
    print('Giải mã từng khối: m_i=c_i^d mod n')
    try:text,decoded=decrypt_text(blocks,key['n'],key['d'])
    except (ValueError,UnicodeDecodeError) as exc:raise SystemExit(str(exc))
    for i,(c,byte) in enumerate(zip(blocks,decoded),1):
        print(f"Byte {i}: m_{i}={c}^{key['d']} mod {key['n']}={byte}")
    print('Ghép các byte rồi giải mã UTF-8.')
    print('NỘI DUNG BOB ĐỌC ĐƯỢC:',text)
    out=ROOT/'results';out.mkdir(exist_ok=True)
    (out/'bob_received.txt').write_text(text,encoding='utf-8')
    print('Đã lưu nội dung sau giải mã vào results/bob_received.txt')
if __name__=='__main__':main()
