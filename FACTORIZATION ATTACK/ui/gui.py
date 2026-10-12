import tkinter as tk
from tkinter import messagebox
import time
from core.math_utils import find_prime_factors, mod_inverse

# Import matplotlib tích hợp vào Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches

# Bộ test từ bé đến lớn
BENCHMARK_SUITE = [
    ("Siêu nhỏ (~12b)", 3233, 17),
    ("Nhỏ (~37b)", 100008300017, 65537),
    ("Vừa (~50b)", 1000004200000437, 65537),
    ("Trung bình (~57b)", 100000082000001557, 65537),
    ("Lớn (~52b)", 2500004400001927, 65537),
    ("Rất lớn (~54b)", 10000004400000259, 65537),
]

def draw_flowchart(ax, canvas, n, e, p, q, phi, d, factor_time):
    """Vẽ sơ đồ khối quy trình phân tích nhân tử và tìm khóa bí mật."""
    ax.clear()
    ax.axis("off")

    steps = [
        {"title": "INPUT (Public Key)", "desc": f"N = {n}\ne = {e}", "color": "#E3F2FD"},
        {"title": "BƯỚC 1: Phân tích N", "desc": f"p = {p}\nq = {q}\n⏱ {factor_time*1000:.2f} ms", "color": "#FFF9C4"},
        {"title": "BƯỚC 2: Euler Phi", "desc": f"Φ(N) = (p-1)(q-1)\n= {phi}", "color": "#FFE0B2"},
        {"title": "OUTPUT (Private Key)", "desc": f"d ≡ e⁻¹ mod Φ(N)\nd = {d}", "color": "#C8E6C9"}
    ]

    y_pos = 0.85
    for i, step in enumerate(steps):
        # Vẽ hộp khối
        rect = patches.FancyBboxPatch(
            (0.1, y_pos - 0.12), 0.8, 0.14,
            boxstyle="round,pad=0.03",
            edgecolor="#333333", facecolor=step["color"], linewidth=1.5
        )
        ax.add_patch(rect)
        ax.text(0.5, y_pos - 0.02, step["title"], fontsize=9, fontweight="bold", ha="center")
        ax.text(0.5, y_pos - 0.08, step["desc"], fontsize=8, ha="center", fontfamily="monospace")

        # Vẽ mũi tên liên kết giữa các khối
        if i < len(steps) - 1:
            ax.annotate(
                "", xy=(0.5, y_pos - 0.19), xytext=(0.5, y_pos - 0.13),
                arrowprops=dict(facecolor="#555555", edgecolor="#555555", width=1.5, headwidth=6)
            )
        y_pos -= 0.24

    ax.set_ylim(-0.15, 0.95)
    ax.set_xlim(0, 1)
    canvas.draw()

def draw_benchmark_chart(ax, canvas, labels, times):
    """Vẽ biểu đồ cột so sánh thời gian giải từ bé đến lớn."""
    ax.clear()
    ax.axis("on")
    bars = ax.barh(labels, times, color="#42A5F5", edgecolor="#1E88E5")
    ax.set_xlabel("Thời gian thực thi (giây)", fontsize=8)
    ax.set_title("So sánh thời gian phân tích theo kích thước N", fontsize=9, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.6)

    # Hiển thị nhãn thời gian trên từng cột
    for bar in bars:
        w = bar.get_width()
        val_str = f"{w*1000:.1f}ms" if w < 1 else f"{w:.2f}s"
        ax.text(w + max(times)*0.02, bar.get_y() + bar.get_height()/2, val_str,
                va='center', fontsize=7, fontweight="bold")

    ax.set_xlim(0, max(times) * 1.25 if max(times) > 0 else 1)
    plt.tight_layout()
    canvas.draw()

def run_single(entry_n, entry_e, text_output, ax, canvas):
    try:
        n = int(entry_n.get().strip())
        e = int(entry_e.get().strip())
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ!")
        return

    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, f"=== BẮT ĐẦU TẤN CÔNG N = {n} ===\n")
    
    t0 = time.perf_counter()
    p, q, factor_time = find_prime_factors(n)
    
    if not p:
        text_output.insert(tk.END, f"❌ Không thể phân tích (Duyệt hết căn bậc 2 trong {factor_time:.4f}s)\n")
        return
        
    phi_n = (p - 1) * (q - 1)
    d = mod_inverse(e, phi_n)
    total_time = time.perf_counter() - t0
    
    text_output.insert(tk.END, f"✓ p = {p}\n✓ q = {q}\n")
    text_output.insert(tk.END, f"✓ Φ(N) = {phi_n}\n")
    text_output.insert(tk.END, f"✓ Khóa bí mật d = {d}\n")
    text_output.insert(tk.END, f"⏱️ Thời gian tìm nhân tử: {factor_time * 1000:.3f} ms\n")
    text_output.insert(tk.END, f"⏱️ Tổng thời gian: {total_time * 1000:.3f} ms\n")

    # Vẽ sơ đồ quy trình
    draw_flowchart(ax, canvas, n, e, p, q, phi_n, d, factor_time)

def run_benchmark(text_output, root, ax, canvas):
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, "🚀 ĐANG CHẠY SO SÁNH TỪ BÉ ĐẾN LỚN...\n")
    root.update()

    labels, times = [], []
    for name, n, e in BENCHMARK_SUITE:
        text_output.insert(tk.END, f"Đang giải {name} (N={n})...\n")
        root.update()

        p, q, factor_time = find_prime_factors(n)
        labels.append(name)
        times.append(factor_time)

        res = f"{factor_time*1000:.2f} ms" if factor_time < 1 else f"{factor_time:.2f} s"
        text_output.insert(tk.END, f"  -> Xong trong: {res}\n")
        root.update()

    text_output.insert(tk.END, "✅ HOÀN THÀNH!\n")
    draw_benchmark_chart(ax, canvas, labels, times)

def create_app():
    root = tk.Tk()
    root.title("RSA Factorization Attack - Visualizer")
    root.geometry("980x680")
    root.configure(padx=10, pady=10)

    # Chia 2 cột: Cột trái (Điều khiển & Text), Cột phải (Sơ đồ trực quan)
    pane_left = tk.Frame(root, width=460)
    pane_left.pack(side="left", fill="both", expand=True, padx=(0, 10))

    pane_right = tk.Frame(root, width=480)
    pane_right.pack(side="right", fill="both", expand=True)

    # --- CỘT TRÁI ---
    frame_input = tk.LabelFrame(pane_left, text="Nhập Khóa Công Khai", padx=8, pady=8)
    frame_input.pack(fill="x", pady=(0, 8))

    tk.Label(frame_input, text="Modulus (N):").grid(row=0, column=0, sticky="w")
    entry_n = tk.Entry(frame_input, width=30)
    entry_n.grid(row=0, column=1, padx=5, pady=3)
    entry_n.insert(0, "3233")

    tk.Label(frame_input, text="Public Exponent (e):").grid(row=1, column=0, sticky="w")
    entry_e = tk.Entry(frame_input, width=30)
    entry_e.grid(row=1, column=1, padx=5, pady=3)
    entry_e.insert(0, "17")

    btn_single = tk.Button(
        frame_input, text="🚀 Chạy & Vẽ Sơ Đồ", bg="#4CAF50", fg="white", font=("Arial", 9, "bold"),
        command=lambda: run_single(entry_n, entry_e, text_output, ax, canvas)
    )
    btn_single.grid(row=0, column=2, rowspan=2, padx=8)

    btn_batch = tk.Button(
        pane_left, text="📊 Chạy So Sánh Dãy & Vẽ Đồ Thị Thời Gian", bg="#ff4d4d", fg="white", font=("Arial", 10, "bold"),
        command=lambda: run_benchmark(text_output, root, ax, canvas)
    )
    btn_batch.pack(fill="x", pady=(0, 8))

    frame_text = tk.LabelFrame(pane_left, text="Nhật ký chi tiết", padx=8, pady=8)
    frame_text.pack(fill="both", expand=True)
    text_output = tk.Text(frame_text, wrap="word", font=("Consolas", 9))
    text_output.pack(fill="both", expand=True)

    # --- CỘT PHẢI: KHU VỰC VẼ SƠ ĐỒ ---
    frame_chart = tk.LabelFrame(pane_right, text="Sơ Đồ Luồng / Đồ Thị Trực Quan", padx=5, pady=5)
    frame_chart.pack(fill="both", expand=True)

    fig, ax = plt.subplots(figsize=(4.8, 5.8), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=frame_chart)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Vẽ sơ đồ mặc định ban đầu
    ax.text(0.5, 0.5, "Nhập N và bấm nút\nđể tạo sơ đồ quy trình", ha="center", va="center", color="#888888")
    ax.axis("off")
    canvas.draw()

    return root