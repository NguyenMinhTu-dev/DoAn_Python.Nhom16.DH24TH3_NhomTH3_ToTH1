import sys
import os

# === BƯỚC 1: SỬA LỖI IMPORT (Thêm 6 dòng này) ===
# Lấy đường dẫn đến thư mục 'gui' (nơi file này đang ở)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Lấy đường dẫn đến thư mục cha (thư mục 'src' hoặc 'DoAn')
parent_dir = os.path.dirname(current_dir)

# Thêm thư mục cha vào sys.path để Python có thể tìm thấy thư mục 'models'
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
# ========================================

# === CÁC IMPORT CHUẨN CỦA DỰ ÁN (DÙNG TTKBOOTSTRAP) ===
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from tkinter import messagebox

# (Import main_window và user_model - bây giờ sẽ hoạt động)
# Đảm bảo file main_window.py nằm CÙNG CẤP với file Login.py
try:
    from main_window import Application
    from models.user_model import check_login_credentials
except ImportError as e:
    messagebox.showerror("Lỗi Import",
                         f"Không tìm thấy file 'main_window' hoặc 'models'.\nLỗi: {e}\n\nHãy đảm bảo 6 dòng sys.path ở đầu file Login.py là chính xác.")
    sys.exit()

# --- ĐỊNH NGHĨA MÀU SẮC ---
COLOR_BACKGROUND = "#00C4C4"
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY = "#00A79E"
COLOR_TEXT = "#333333"
COLOR_SUBTEXT = "#555555"
COLOR_BORDER = "#B0B0B0"
COLOR_MAIN_BG = "#F8F9FA"  # Cần cho việc đổi nền sau login

# --- KHỞI TẠO CỬA SỔ CHÍNH (CHỈ 1 LẦN) ---
# Sửa lỗi Theme: Thêm themename="cosmo"
app = ttk.Window(title="Đăng Nhập Hệ Thống", themename="cosmo")
app.geometry("900x600")  # Bắt đầu với kích thước của Login
app.configure(background=COLOR_BACKGROUND)

# Tạo Style CHUNG cho toàn ứng dụng
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


# --- HÀM CHECK_LOGIN (Gọi Model) ---
def check_login():
    user = username_entry.get()
    password = password_entry.get()

    # Gọi hàm logic từ model
    if check_login_credentials(user, password):
        # ĐĂNG NHẬP THÀNH CÔNG

        # 1. Xóa Frame Đăng Nhập (card_frame)
        card_frame.destroy()

        # 2. Thay đổi kích thước và tiêu đề của cửa sổ 'app'
        app.geometry("1400x800")
        app.title("Hệ Thống Quản Lý")
        app.configure(background=COLOR_MAIN_BG)  # Đổi nền thành xám nhạt

        # 3. Tạo và vẽ Frame Chính (Application)
        # Sửa lỗi Theme: Truyền 'style' (đã tạo ở trên) vào Application
        main_ui = Application(app, style=style)
        main_ui.pack(fill="both", expand=True)

    else:
        # ĐĂNG NHẬP THẤT BẠI
        messagebox.showerror("Đăng nhập thất bại", "Sai tên đăng nhập hoặc mật khẩu.")


# --- FRAME ĐĂNG NHẬP (ĐẶT TÊN LÀ 'card_frame') ---
card_frame = ttk.Frame(app, padding=40)
card_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# --- NỘI DUNG TRONG CARD ---
ttk.Label(card_frame, text="XANH SM",
          font=("Arial", 28, "bold"),
          foreground=COLOR_PRIMARY).pack(pady=(20, 10))
ttk.Label(card_frame, text="Đăng nhập để tiếp tục",
          font=("Arial", 11),
          foreground=COLOR_SUBTEXT).pack(pady=(0, 30))

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

login_button = ttk.Button(card_frame, text="Đăng Nhập", style='Primary.TButton',
                          command=check_login)  # Gán lệnh
login_button.pack(fill='x', padx=10, pady=(35, 10))

forgot_label = ttk.Label(card_frame, text="Quên mật khẩu?",
                         font=("Arial", 10, "underline"),
                         foreground=COLOR_SUBTEXT,
                         cursor="hand2")
forgot_label.pack(pady=10)

# --- CHẠY ỨNG DỤNG ---
if __name__ == "__main__":
    username_entry.focus_set()
    app.mainloop()