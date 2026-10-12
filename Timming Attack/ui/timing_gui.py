import tkinter as tk
from tkinter import messagebox
import string
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core.timing_engine import VulnerableServer, measure_average_time

def draw_timing_bar(ax, canvas, charset, times, chosen_char):
    """Vẽ biểu đồ thời gian của các ký tự ứng viên tại vị trí đang dò."""
    ax.clear()
    ax.axis("on")
    
    colors = ['#4CAF50' if c == chosen_char else '#90CAF9' for c in charset]
    times_ms = [t * 1000 for t in times]
    
    bars = ax.bar(list(charset), times_ms, color=colors, edgecolor="#1565C0")
    ax.set_ylabel("Thời gian (ms)", fontsize=8, fontweight="bold")
    ax.set_xlabel("Ký tự thử nghiệm", fontsize=8, fontweight="bold")
    ax.set_title(f"Phân tích thời gian - Ký tự chọn: '{chosen_char}'", fontsize=9, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    # Hiển thị số liệu trên cột cao nhất
    if times_ms:
        max_idx = times_ms.index(max(times_ms))
        ax.text(max_idx, max(times_ms) + 0.1, f"{max(times_ms):.1f}ms", 
                ha="center", fontsize=8, fontweight="bold", color="#2E7D32")

    canvas.draw()

def start_timing_attack(entry_secret, entry_samples, text_output, root, ax, canvas):
    secret = entry_secret.get().strip()
    try:
        samples = int(entry_samples.get().strip())
    except ValueError:
        messagebox.showerror("Lỗi", "Số lượng mẫu phải là số nguyên!")
        return

    if not secret:
        messagebox.showerror("Lỗi", "Vui lòng nhập chuỗi bí mật cần kiểm thử!")
        return

    server = VulnerableServer(secret)
    length = len(secret)
    charset = string.digits  # Thử nghiệm trên các chữ số 0-9

    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, "=== BẮT ĐẦU TIMING ATTACK ===\n")
    text_output.insert(tk.END, f"Mục tiêu: Tìm chuỗi bí mật có độ dài {length}\n\n")

    # BƯỚC 1: Đo Baseline với input sai hoàn toàn
    wrong_input = "x" * length
    t_base = measure_average_time(server, wrong_input, samples=samples)
    text_output.insert(tk.END, f"[BƯỚC 1] Đo baseline với input sai ('{wrong_input}'):\n")
    text_output.insert(tk.END, f"  ⏱️ T_base = {t_base * 1000:.3f} ms\n\n")
    root.update()

    # BƯỚC 2 & 3: Dò từng vị trí
    discovered = ""
    for pos in range(length):
        text_output.insert(tk.END, f"[BƯỚC 2] Đang dò vị trí {pos + 1}/{length}...\n")
        root.update()

        times_record = []
        best_char = None
        max_time = -1.0

        for char in charset:
            # Ghép chuỗi thử nghiệm: tiền tố đã tìm + ký tự thử + đệm placeholder
            candidate = discovered + char + "0" * (length - len(discovered) - 1)
            avg_time = measure_average_time(server, candidate, samples=samples)
            times_record.append(avg_time)

            if avg_time > max_time:
                max_time = avg_time
                best_char = char

        discovered += best_char
        text_output.insert(tk.END, f"  -> Chọn '{best_char}' (thời gian cao nhất: {max_time * 1000:.3f} ms)\n")
        text_output.insert(tk.END, f"  -> Chuỗi hiện tại: {discovered}\n\n")
        root.update()

        # Vẽ biểu đồ cập nhật tại vị trí này
        draw_timing_bar(ax, canvas, charset, times_record, best_char)

    # BƯỚC 3: Kết luận
    text_output.insert(tk.END, "=== KẾT QUẢ OUTPUT ===\n")
    text_output.insert(tk.END, f"Chuỗi bí mật tìm được: {discovered}\n")
    text_output.insert(tk.END, f"Trạng thái: {'THÀNH CÔNG' if discovered == secret else 'THẤT BẠI'}\n")

def create_timing_app():
    root = tk.Tk()
    root.title("Timing Attack Simulation - Side-Channel Analysis")
    root.geometry("980x680")
    root.configure(padx=10, pady=10)

    pane_left = tk.Frame(root, width=460)
    pane_left.pack(side="left", fill="both", expand=True, padx=(0, 10))

    pane_right = tk.Frame(root, width=500)
    pane_right.pack(side="right", fill="both", expand=True)

    # Khung cấu hình
    frame_cfg = tk.LabelFrame(pane_left, text="Cấu hình hệ thống mục tiêu", padx=8, pady=8)
    frame_cfg.pack(fill="x", pady=(0, 8))

    tk.Label(frame_cfg, text="Secret PIN/Key:").grid(row=0, column=0, sticky="w")
    entry_secret = tk.Entry(frame_cfg, width=20)
    entry_secret.grid(row=0, column=1, padx=5, pady=3)
    entry_secret.insert(0, "7419")

    tk.Label(frame_cfg, text="Số mẫu lấy trung bình:").grid(row=1, column=0, sticky="w")
    entry_samples = tk.Entry(frame_cfg, width=20)
    entry_samples.grid(row=1, column=1, padx=5, pady=3)
    entry_samples.insert(0, "15")

    btn_attack = tk.Button(
        frame_cfg, text="🚀 BẮT ĐẦU DÒ THỜI GIAN", bg="#D32F2F", fg="white", font=("Arial", 9, "bold"),
        command=lambda: start_timing_attack(entry_secret, entry_samples, text_output, root, ax, canvas)
    )
    btn_attack.grid(row=2, column=0, columnspan=2, pady=8)

    # Nhật ký
    frame_text = tk.LabelFrame(pane_left, text="Quá trình thực thi & Baseline", padx=8, pady=8)
    frame_text.pack(fill="both", expand=True)
    text_output = tk.Text(frame_text, wrap="word", font=("Consolas", 9))
    text_output.pack(fill="both", expand=True)

    # Khung biểu đồ
    frame_chart = tk.LabelFrame(pane_right, text="Biểu Đồ Phân Phối Thời Gian Ứng Viên", padx=5, pady=5)
    frame_chart.pack(fill="both", expand=True)

    fig, ax = plt.subplots(figsize=(5.0, 5.8), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=frame_chart)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    ax.text(0.5, 0.5, "Bấm 'BẮT ĐẦU DÒ THỜI GIAN'\nđể xem biểu đồ phân tích", ha="center", va="center", color="#777777")
    ax.axis("off")
    canvas.draw()

    return root