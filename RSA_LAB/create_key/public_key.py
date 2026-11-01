import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *
k=read('private_key.json');pub=read('public_key.json')
print('Trình bày lại bước Bob tạo PUBLIC KEY, dùng dữ liệu phía Bob:')
print(f"p={k['p']}, q={k['q']}; n=pq={pub['n']}")
print(f"phi=(p-1)(q-1)={k['phi']}; e={pub['e']}; gcd(e,phi)={math.gcd(pub['e'],k['phi'])}")
print('Public key chỉ công bố n,e:',pub)
