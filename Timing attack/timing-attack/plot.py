import csv
import matplotlib.pyplot as plt

prefix, unsafe, safe = [], [], []
with open('results/timing_result.csv') as f:
    for row in csv.DictReader(f):
        prefix.append(int(row['prefix_correct']))
        unsafe.append(int(row['time_unsafe_ns']))
        safe.append(int(row['time_safe_ns']))

plt.figure(figsize=(10, 6))
plt.plot(prefix, unsafe, 'ro-', linewidth=2, markersize=8, label='Unsafe (thoat som)')
plt.plot(prefix, safe, 'bo-', linewidth=2, markersize=8, label='Safe (constant-time)')
plt.xlabel('So ky tu dung prefix', fontsize=12)
plt.ylabel('Thoi gian (ns)', fontsize=12)
plt.title('Timing Attack: Unsafe vs Safe', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('results/timing_chart.png', dpi=150, bbox_inches='tight')
print('Da luu: results/timing_chart.png')
