import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# --- BƯỚC 1: THÊM IMPORTS ---
from tkinter import messagebox
from main_window import Application

# --- ĐỊNH NGHĨA CÁC MÃ MÀU CHỦ ĐẠO ---
COLOR_BACKGROUND = "#00C4C4"
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY = "#00A79E"
COLOR_TEXT = "#333333"
COLOR_SUBTEXT = "#555555"
COLOR_BORDER = "#B0B0B0"

# --- KHỞI TẠO CỬA SỔ LOGIN ---
# (Tên biến 'app' là cửa sổ Login)
app = ttk.Window(title="Đăng Nhập Hệ Thống")
app.geometry("900x600")
app.resizable(True, True)
app.configure(background=COLOR_BACKGROUND)

# (Toàn bộ code Style của bạn giữ nguyên)
style = Style()
style.configure('TFrame', background=COLOR_CARD)
style.configure('TLabel', background=COLOR_CARD, foreground=COLOR_TEXT)
style.configure('TButton', font=("Arial", 14, "bold"), padding=10)
style.configure('Primary.TButton', background=COLOR_PRIMARY, foreground="white", borderwidth=0)
style.map('Primary.TButton',
          background=[('active', '#007A72')])
style.configure('TEntry',
                fieldbackground=COLOR_CARD,
                foreground=COLOR_TEXT,
                borderwidth=1,
                padding=10)
style.map('TEntry',
          bordercolor=[('focus', COLOR_PRIMARY),
                       ('!focus', COLOR_BORDER)],
          relief=[('focus', 'solid'), ('!focus', 'solid')]
          )

# --- FRAME ĐĂNG NHẬP CHÍNH (CĂN GIỮA) ---
card_frame = ttk.Frame(app, padding=40)
card_frame.place(relx=0.5, rely=0.5, anchor=CENTER)


# --- BƯỚC 2: TẠO HÀM CHECK_LOGIN ---
def check_login():
    user = username_entry.get()
    password = password_entry.get()

    if user == "admin" and password == "123":
        # ĐĂNG NHẬP THÀNH CÔNG
        # 1. Đóng cửa sổ Login (biến 'app')
        app.destroy()

        # 2. Mở cửa sổ Main (Application)
        main_app = Application(themename="cosmo")
        main_app.mainloop()
    else:
        # ĐĂNG NHẬP THẤT BẠI
        messagebox.showerror("Đăng nhập thất bại", "Sai tên đăng nhập hoặc mật khẩu.")


# --- NỘI DUNG TRONG CARD ---

# 1. Tiêu đề
ttk.Label(card_frame, text="XANH SM",
          font=("Arial", 28, "bold"),
          foreground=COLOR_PRIMARY).pack(pady=(20, 10))
# ... (các label khác)
ttk.Label(card_frame, text="Đăng nhập để tiếp tục",
          font=("Arial", 11),
          foreground=COLOR_SUBTEXT).pack(pady=(0, 30))

# 2. Ô Nhập Liệu
ttk.Label(card_frame, text="TÀI KHOẢN",
          font=("Arial", 10, "bold"),
          foreground=COLOR_SUBTEXT).pack(anchor='w', padx=10)
username_entry = ttk.Entry(card_frame, font=("Arial", 12), width=35)
username_entry.pack(fill='x', padx=10, ipady=5)

ttk.Label(card_frame, text="MẬT KHẨU",
          font=("Arial", 10, "bold"),
          foreground=COLOR_SUBTEXT).pack(anchor='w', padx=10, pady=(20, 0))
password_entry = ttk.Entry(card_frame, show="*", font=("Arial", 12))
password_entry.pack(fill='x', padx=10, ipady=5)

# --- BƯỚC 3: GÁN COMMAND CHO NÚT ---
login_button = ttk.Button(card_frame, text="Đăng Nhập", style='Primary.TButton',
                          command=check_login)  # <--- THÊM COMMAND VÀO ĐÂY
login_button.pack(fill='x', padx=10, pady=(35, 10))

# 4. Quên mật khẩu
forgot_label = ttk.Label(card_frame, text="Quên mật khẩu?",
                         font=("Arial", 10, "underline"),
                         foreground=COLOR_SUBTEXT,
                         cursor="hand2")
forgot_label.pack(pady=10)

# --- CHẠY ỨNG DỤNG ---
username_entry.focus_set()
app.mainloop()