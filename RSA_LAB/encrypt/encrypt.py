import sys,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *

def encrypt_text(text,n,e):
    if n<=255:raise ValueError('Minh họa UTF-8 theo byte cần n>255. Hãy tạo khóa mặc định.')
    return [pow(byte,e,n) for byte in text.encode('utf-8')]

def main():
    parser=argparse.ArgumentParser(description='Alice mã hóa văn bản bằng public key Bob')
    parser.add_argument('--text',default='Hello Bob');a=parser.parse_args()
    pub=read('public_key.json');n,e=pub['n'],pub['e']
    try:blocks=encrypt_text(a.text,n,e)
    except ValueError as exc:parser.error(str(exc))
    print('ALICE — TRƯỚC KHI GỬI')
    print('Nội dung chỉ Alice đang nhập:',repr(a.text))
    print(f'Dùng PUBLIC KEY Bob: n={n}, e={e}')
    print('Chuyển văn bản thành byte UTF-8, mỗi byte m_i được mã hóa: c_i=m_i^e mod n')
    for i,(byte,c) in enumerate(zip(a.text.encode('utf-8'),blocks),1):
        print(f'Byte {i}: c_{i}={byte}^{e} mod {n}={c}')
    # Không ghi text hoặc byte bản rõ vào gói gửi đi.
    write('alice_to_bob.json',{'format':'textbook-rsa-utf8-byte-v1','n':n,'e':e,'ciphertext_blocks':blocks})
    print('\nTRÊN ĐƯỜNG TRUYỀN — CHỈ GỬI BẢN MÃ')
    print(blocks)
    print('Gói data/alice_to_bob.json không chứa trường bản rõ.')
    print('Bob chạy: python decrypt/decrypt.py')
if __name__=='__main__':main()
