import tkinter as tk
from tkinter import font as tkfont
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

from src.models.dashbroad_model import DashbroadPage

# Import các trang con
# Nếu thiếu 1 trong 4 file này, chương trình sẽ báo lỗi
try:
    from dashbroad import DashbroadPage
    from vehicle_page import VehiclePage
    from driver_page import DriverPage
    from customer_page import CustomerPage
except ImportError as e:
    # Lỗi này sẽ xuất hiện nếu bạn thiếu file hoặc CHƯA CÀI MATPLOTLIB
    print(f"LỖI IMPORT TRANG CON: {e}")
    print("Hãy đảm bảo bạn đã tạo đủ 4 file và CÀI ĐẶT MATPLOTLIB (pip install matplotlib)")
    exit()

# --- Định nghĩa màu sắc (Dùng chung) ---
COLOR_SIDEBAR_BG = "#FFFFFF"
COLOR_MAIN_BG = "#F8F9FA"
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY_TEAL = "#00A79E"
COLOR_ACTIVE_BG = "#E0F7FA"
COLOR_ACTIVE_FG = "#00A79E"
COLOR_SIDEBAR_FG = "#333333"


# --- LỚP ỨNG DỤNG CHÍNH (TÊN LÀ APPLICATION) ---
# === SỬA KẾ THỪA: TỪ 'ttk.Window' THÀNH 'ttk.Frame' ===
class Application(ttk.Frame):
    # Hàm __init__ phải nhận 'parent' và 'style'
    def __init__(self, parent, style, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.style = style  # <-- Lưu lại style từ Login

        self.configure(style="TFrame")

        self.setup_styles()

        # --- Bố Cục Chính (Sidebar và Content) ---
        self.sidebar_frame = self.create_sidebar()
        self.sidebar_frame.pack(side="left", fill="y")

        self.content_frame = ttk.Frame(self, bootstyle="light")
        self.content_frame.pack(side="right", fill="both", expand=True)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # --- Quản lý các Trang ---
        self.frames = {}
        for F in (DriverPage, VehiclePage, CustomerPage, DashbroadPage):
            page_name = F.__name__
            frame = F(self.content_frame, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("DashbroadPage")

    def setup_styles(self):
        # Dùng style được truyền vào
        style = self.style

        style.configure('primary.TFrame', background=COLOR_SIDEBAR_BG)
        style.configure('TFrame', background=COLOR_MAIN_BG)
        style.configure('light.TFrame', background=COLOR_CARD)
        style.configure('TLabel', background=COLOR_MAIN_BG, foreground="#333")
        style.configure('light.TLabel', background=COLOR_CARD, foreground="#333333")

        sidebar_font = tkfont.Font(family="Arial", size=11, weight="bold")

        # Nút Thường
        style.configure('Sidebar.TButton',
                        font=sidebar_font,
                        foreground=COLOR_SIDEBAR_FG,
                        background=COLOR_SIDEBAR_BG,
                        anchor="w",
                        padding=(15, 12),
                        borderwidth=0)
        style.map('Sidebar.TButton',
                  background=[('active', COLOR_ACTIVE_BG),
                              ('!active', COLOR_SIDEBAR_BG)])

        # Nút Được Chọn (Active)
        style.configure('Active.TButton',
                        font=sidebar_font,
                        foreground=COLOR_ACTIVE_FG,
                        background=COLOR_ACTIVE_BG,
                        anchor="w",
                        padding=(15, 12),
                        borderwidth=0)
        style.map('Active.TButton',
                  background=[('active', COLOR_ACTIVE_BG), ('!active', COLOR_ACTIVE_BG)])

    def create_sidebar(self):
        sidebar = ttk.Frame(self, width=280, style="primary")
        sidebar.pack_propagate(False)

        ttk.Label(sidebar, text="XANH SM",
                  font=("Arial", 22, "bold"),
                  foreground=COLOR_PRIMARY_TEAL,
                  background=COLOR_SIDEBAR_BG).pack(pady=30, padx=20)

        self.nav_buttons = {}
        nav_items = [
            ("DashbroadPage", "Tổng Quan"),
            ("DriverPage", "Quản Lý Tài Xế"),
            ("VehiclePage", "Quản Lý Phương Tiện"),
            ("CustomerPage", "Quản Lý Khách Hàng")
        ]

        for page_name, text in nav_items:
            btn = ttk.Button(sidebar, text=text, style='Sidebar.TButton',
                             command=lambda p=page_name: self.show_frame(p))
            btn.pack(fill="x", padx=20, pady=5)
            self.nav_buttons[page_name] = btn

        return sidebar

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configure(style='Active.TButton')
            else:
                button.configure(style='Sidebar.TButton')

# File này là thư viện nên KHÔNG CẦN 'if __name__ == "__main__":'