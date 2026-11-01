import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *
k=read('private_key.json');pub=read('public_key.json')
print('Bob tính d=e^(-1) mod phi(n):')
d=inverse(pub['e'],k['phi'])
print(f"d={d}; ed={pub['e']*d}=1+{(pub['e']*d-1)//k['phi']} × {k['phi']}")
