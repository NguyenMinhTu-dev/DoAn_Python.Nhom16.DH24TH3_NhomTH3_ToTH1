import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style  # <-- Import Style
from tkinter import messagebox

# Import lớp Application từ file main_window
# (Đảm bảo tên file là main_window.py)
try:
    from main_window import Application
except ImportError:
    messagebox.showerror("Lỗi Import", "Không tìm thấy file 'main_window.py' hoặc lớp 'Application'")
    exit()

# --- Định nghĩa màu sắc ---
COLOR_BACKGROUND = "#00C4C4"
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY = "#00A79E"
COLOR_TEXT = "#333333"
COLOR_SUBTEXT = "#555555"
COLOR_BORDER = "#B0B0B0"
COLOR_MAIN_BG = "#F8F9FA" # Màu nền của main_window

# --- Khởi tạo App và Style (Chỉ 1 lần) ---
app = ttk.Window(title="Đăng Nhập Hệ Thống", themename="cosmo")
app.geometry("900x600")
app.configure(background=COLOR_BACKGROUND)

# Tạo Style object để dùng chung
style = Style()

# Cấu hình style cho trang Login
style.configure('TFrame', background=COLOR_CARD)
style.configure('TLabel', background=COLOR_CARD, foreground=COLOR_TEXT)
style.configure('TButton', font=("Arial", 14, "bold"), padding=10)
style.configure('Primary.TButton', background=COLOR_PRIMARY, foreground="white", borderwidth=0)
style.map('Primary.TButton', background=[('active', '#007A72')])
style.configure('TEntry',
                fieldbackground=COLOR_CARD,
                foreground=COLOR_TEXT,
                borderwidth=1,
                padding=10)
style.map('TEntry',
          bordercolor=[('focus', COLOR_PRIMARY), ('!focus', COLOR_BORDER)],
          relief=[('focus', 'solid'), ('!focus', 'solid')]
          )

# --- Frame Đăng Nhập ---
card_frame = ttk.Frame(app, padding=40)
card_frame.place(relx=0.5, rely=0.5, anchor="center")

def check_login():
    user = username_entry.get()
    password = password_entry.get()

    if user == "admin" and password == "123":
        # 1. Xóa Frame Đăng Nhập
        card_frame.destroy()

        # 2. Thay đổi Cửa Sổ
        app.title("Hệ thống quản lý Xanh SM")
        app.geometry("1400x800") # Đổi kích thước
        app.configure(background=COLOR_MAIN_BG) # Đổi nền

        # 3. Mở giao diện chính VÀ TRUYỀN STYLE VÀO
        main_ui = Application(app, style=style)  # <-- Truyền 'style' vào đây
        main_ui.pack(fill="both", expand=True)

    else:
        messagebox.showerror("Đăng nhập thất bại", "Sai tên đăng nhập hoặc mật khẩu.")

# --- Các Widget của Login ---
ttk.Label(card_frame, text="XANH SM", font=("Arial", 28, "bold"),
          foreground=COLOR_PRIMARY).pack(pady=(20, 10))
ttk.Label(card_frame, text="Đăng nhập để tiếp tục", font=("Arial", 11),
          foreground=COLOR_SUBTEXT).pack(pady=(0, 30))

ttk.Label(card_frame, text="TÀI KHOẢN", font=("Arial", 10, "bold"),
          foreground=COLOR_SUBTEXT).pack(anchor='w', padx=10)
username_entry = ttk.Entry(card_frame, font=("Arial", 12), width=35)
username_entry.pack(fill='x', padx=10, ipady=5)

ttk.Label(card_frame, text="MẬT KHOẢU", font=("Arial", 10, "bold"),
          foreground=COLOR_SUBTEXT).pack(anchor='w', padx=10, pady=(20, 0))
password_entry = ttk.Entry(card_frame, show="*", font=("Arial", 12))
password_entry.pack(fill='x', padx=10, ipady=5)

login_button = ttk.Button(card_frame, text="Đăng Nhập", style='Primary.TButton', # Đổi style cho đẹp
                          command=check_login)
login_button.pack(fill='x', padx=10, pady=(35, 10))

username_entry.focus_set()
app.mainloop()