import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches

from core.cca_engine import execute_cca, DecryptionOracle

def draw_pipeline(ax, canvas, c_star, s, c_prime, m_prime, s_inv, m_star):
    """Vẽ Pipeline trực quan quy trình Blinding -> Oracle -> Unblinding."""
    ax.clear()
    ax.axis("off")

    steps = [
        {"title": "MỤC TIÊU BAN ĐẦU", "desc": f"Ciphertext c* = {c_star}", "color": "#FFCDD2"},
        {"title": "BƯỚC 1: BLINDING", "desc": f"s = {s}\nc' = c* · s^e mod n\n= {c_prime}", "color": "#FFE0B2"},
        {"title": "BƯỚC 2: DECRYPTION ORACLE", "desc": f"m' = (c')^d mod n\n= {m_prime}", "color": "#FFF9C4"},
        {"title": "BƯỚC 3: UNBLINDING", "desc": f"s⁻¹ mod n = {s_inv}\nm* = m' · s⁻¹ mod n\n= {m_star}", "color": "#C8E6C9"}
    ]

    y = 0.88
    for i, step in enumerate(steps):
        rect = patches.FancyBboxPatch(
            (0.08, y - 0.13), 0.84, 0.14,
            boxstyle="round,pad=0.02",
            edgecolor="#333333", facecolor=step["color"], linewidth=1.5
        )
        ax.add_patch(rect)
        ax.text(0.5, y - 0.02, step["title"], fontsize=9, fontweight="bold", ha="center")
        ax.text(0.5, y - 0.08, step["desc"], fontsize=7.5, ha="center", fontfamily="monospace")

        if i < len(steps) - 1:
            ax.annotate(
                "", xy=(0.5, y - 0.20), xytext=(0.5, y - 0.14),
                arrowprops=dict(facecolor="#555555", edgecolor="#555555", width=1.5, headwidth=6)
            )
        y -= 0.24

    ax.set_ylim(-0.15, 0.95)
    ax.set_xlim(0, 1)
    canvas.draw()

def run_attack(entry_n, entry_e, entry_d, entry_c, text_output, ax, canvas):
    try:
        n = int(entry_n.get().strip())
        e = int(entry_e.get().strip())
        d = int(entry_d.get().strip()) # Khóa ngầm định của Oracle để mô phỏng
        c_star = int(entry_c.get().strip())

        # Khởi tạo Oracle
        oracle = DecryptionOracle(d=d, n=n, forbidden_c=c_star)

        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, "=== TIẾN HÀNH CHOSEN-CIPHERTEXT ATTACK (CCA) ===\n")
        text_output.insert(tk.END, f"Input: n = {n}, e = {e}\n")
        text_output.insert(tk.END, f"Bản mã mục tiêu: c* = {c_star}\n\n")

        # Thực thi quy trình
        res = execute_cca(n, e, c_star, oracle)

        text_output.insert(tk.END, "[Bước 1: Làm mù (Blinding)]\n")
        text_output.insert(tk.END, f"  - Chọn ngẫu nhiên s = {res['s']}\n")
        text_output.insert(tk.END, f"  - Tính s^e mod n = {res['s_e']}\n")
        text_output.insert(tk.END, f"  - Bản mã ngụy trang c' = (c* * s^e) mod n = {res['c_prime']}\n\n")

        text_output.insert(tk.END, "[Bước 2: Gửi Oracle]\n")
        text_output.insert(tk.END, f"  - Gửi c' lên Decryption Oracle (hợp lệ vì c' ≠ c*)\n")
        text_output.insert(tk.END, f"  - Oracle trả về m' = {res['m_prime']}\n\n")

        text_output.insert(tk.END, "[Bước 3: Khôi phục bản rõ (Unblinding)]\n")
        text_output.insert(tk.END, f"  - Tính nghịch đảo modulo: s⁻¹ mod n = {res['s_inv']}\n")
        text_output.insert(tk.END, f"  - Tính m* = (m' * s⁻¹) mod n = {res['recovered_m']}\n\n")

        text_output.insert(tk.END, "=== KẾT QUẢ OUTPUT ===\n")
        text_output.insert(tk.END, f"🎉 Bản rõ gốc m* đã bị giải mã thành công: {res['recovered_m']}\n")

        # Cập nhật pipeline
        draw_pipeline(ax, canvas, c_star, res['s'], res['c_prime'], res['m_prime'], res['s_inv'], res['recovered_m'])

    except ValueError as ve:
        messagebox.showerror("Lỗi", str(ve))

def create_cca_app():
    root = tk.Tk()
    root.title("RSA Chosen-Ciphertext Attack (CCA) Visualizer")
    root.geometry("1020x680")
    root.configure(padx=10, pady=10)

    pane_left = tk.Frame(root, width=470)
    pane_left.pack(side="left", fill="both", expand=True, padx=(0, 10))

    pane_right = tk.Frame(root, width=530)
    pane_right.pack(side="right", fill="both", expand=True)

    # Frame Input
    frame_input = tk.LabelFrame(pane_left, text="Tham số RSA & Bản mã mục tiêu", padx=8, pady=8)
    frame_input.pack(fill="x", pady=(0, 8))

    tk.Label(frame_input, text="Modulus (n):").grid(row=0, column=0, sticky="w")
    entry_n = tk.Entry(frame_input, width=28)
    entry_n.grid(row=0, column=1, padx=5, pady=3)
    entry_n.insert(0, "3233")

    tk.Label(frame_input, text="Public Key (e):").grid(row=1, column=0, sticky="w")
    entry_e = tk.Entry(frame_input, width=28)
    entry_e.grid(row=1, column=1, padx=5, pady=3)
    entry_e.insert(0, "17")

    tk.Label(frame_input, text="Private Key Oracle (d):").grid(row=2, column=0, sticky="w")
    entry_d = tk.Entry(frame_input, width=28)
    entry_d.grid(row=2, column=1, padx=5, pady=3)
    entry_d.insert(0, "2753")

    tk.Label(frame_input, text="Ciphertext mục tiêu (c*):").grid(row=3, column=0, sticky="w")
    entry_c = tk.Entry(frame_input, width=28)
    entry_c.grid(row=3, column=1, padx=5, pady=3)
    entry_c.insert(0, "855")  # 855 là bản mã mã hóa từ m* = 123 (123^17 mod 3233 = 855)

    btn_run = tk.Button(
        frame_input, text="🚀 Thực Thi CCA & Vẽ Pipeline", bg="#D32F2F", fg="white", font=("Arial", 9, "bold"),
        command=lambda: run_attack(entry_n, entry_e, entry_d, entry_c, text_output, ax, canvas)
    )
    btn_run.grid(row=4, column=0, columnspan=2, pady=8)

    # Output Console
    frame_text = tk.LabelFrame(pane_left, text="Quá trình thực thi chi tiết", padx=8, pady=8)
    frame_text.pack(fill="both", expand=True)
    text_output = tk.Text(frame_text, wrap="word", font=("Consolas", 9))
    text_output.pack(fill="both", expand=True)

    # Khung Pipeline đồ họa
    frame_chart = tk.LabelFrame(pane_right, text="Sơ Đồ Pipeline Luồng Dữ Liệu", padx=5, pady=5)
    frame_chart.pack(fill="both", expand=True)

    fig, ax = plt.subplots(figsize=(5.2, 5.8), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=frame_chart)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    ax.text(0.5, 0.5, "Nhấn 'Thực Thi CCA' để xem quá trình\nBlinding -> Oracle -> Unblinding", ha="center", va="center", color="#777777")
    ax.axis("off")
    canvas.draw()

    return root