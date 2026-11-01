import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
scripts=['create_key/create_keys.py','create_key/public_key.py','create_key/private_key.py','encrypt/encrypt.py','decrypt/decrypt.py','attacker/factorization_attack/attack.py','attacker/cca/attack.py','attacker/timing_attack/attack.py']
for script in scripts:
    print('\n>>> '+script,flush=True)
    result=subprocess.run([sys.executable,str(root/script)],cwd=root)
    if result.returncode:
        raise SystemExit(f'{script} kết thúc với mã {result.returncode}. Xem thông báo phía trên.')
print('Hoàn tất. Xem results/ để đọc kết quả và số đo.')
