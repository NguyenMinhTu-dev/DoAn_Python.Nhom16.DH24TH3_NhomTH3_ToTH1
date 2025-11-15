import sys
import os
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# === Sửa lỗi import ===
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# === Import main_window và user_model ===
try:
    from gui.main_window import Application
    from models.user_model import check_login_credentials
except ImportError as e:
    messagebox.showerror(
        "Lỗi Import",
        f"Không tìm thấy file 'main_window' hoặc 'models'.\nLỗi: {e}\nHãy đảm bảo đường dẫn sys.path đúng."
    )
    sys.exit()

# === Màu sắc ===
COLOR_BACKGROUND = "#00C4C4"
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY = "#00A79E"
COLOR_TEXT = "#333333"
COLOR_SUBTEXT = "#555555"
COLOR_BORDER = "#B0B0B0"
COLOR_MAIN_BG = "#F8F9FA"

# === Khởi tạo cửa sổ chính ===
app = ttk.Window(title="Đăng Nhập Hệ Thống", themename="cosmo")
app.geometry("900x600")
app.configure(background=COLOR_BACKGROUND)

# === Style chung ===
style = Style()
style.configure('TFrame', background=COLOR_CARD)
style.configure('TLabel', background=COLOR_CARD, foreground=COLOR_TEXT)
style.configure('TButton', font=("Arial", 14, "bold"), padding=10)
style.configure('Primary.TButton', background=COLOR_PRIMARY, foreground="white", borderwidth=0)
style.map('Primary.TButton', background=[('active', '#007A72')])
style.configure('TEntry', fieldbackground=COLOR_CARD, foreground=COLOR_TEXT, borderwidth=1, padding=10)
style.map('TEntry',
          bordercolor=[('focus', COLOR_PRIMARY), ('!focus', COLOR_BORDER)],
          relief=[('focus', 'solid'), ('!focus', 'solid')])

# === Hàm kiểm tra login ===
def check_login():
    user = username_entry.get().strip()
    password = password_entry.get().strip()

    if not user or not password:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tài khoản và mật khẩu.")
        return

    if check_login_credentials(user, password):
        # Đăng nhập thành công
        card_frame.destroy()
        app.geometry("1400x800")
        app.title("Hệ Thống Quản Lý")
        app.configure(background=COLOR_MAIN_BG)

        main_ui = Application(app, style=style)
        main_ui.pack(fill="both", expand=True)
    else:
        messagebox.showerror("Đăng nhập thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")

# === Frame login ===
card_frame = ttk.Frame(app, padding=40)
card_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

ttk.Label(card_frame, text="Đăng Nhập", font=("Arial", 28, "bold"), foreground=COLOR_PRIMARY).pack(pady=(20, 10))
ttk.Label(card_frame, text="Đăng nhập để tiếp tục", font=("Arial", 11), foreground=COLOR_SUBTEXT).pack(pady=(0, 30))

ttk.Label(card_frame, text="TÀI KHOẢN", font=("Arial", 10, "bold"), foreground=COLOR_SUBTEXT).pack(anchor='w', padx=10)
username_entry = ttk.Entry(card_frame, font=("Arial", 12), width=35)
username_entry.pack(fill='x', padx=10, ipady=5)

ttk.Label(card_frame, text="MẬT KHẨU", font=("Arial", 10, "bold"), foreground=COLOR_SUBTEXT).pack(anchor='w', padx=10, pady=(20, 0))
password_entry = ttk.Entry(card_frame, show="*", font=("Arial", 12))
password_entry.pack(fill='x', padx=10, ipady=5)

login_button = ttk.Button(card_frame, text="Đăng Nhập", style='Primary.TButton', command=check_login)
login_button.pack(fill='x', padx=10, pady=(35, 10))

forgot_label = ttk.Label(card_frame, text="Quên mật khẩu?", font=("Arial", 10, "underline"),
                         foreground=COLOR_SUBTEXT, cursor="hand2")
forgot_label.pack(pady=10)

# === Hàm main để chạy login ===
def main():
    username_entry.focus_set()
    app.mainloop()
