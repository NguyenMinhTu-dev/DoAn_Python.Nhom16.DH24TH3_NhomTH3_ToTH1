import tkinter as tk
from tkinter import font as tkfont
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# Import các trang con
try:
    from gui.dashbroad import DashbroadPage  # Tên trang của bạn
    from gui.vehicle_page import VehiclePage
    from gui.driver_page import DriverPage
    from gui.customer_page import CustomerPage
    from gui.trip_page import TripPage

    # === GIẢ ĐỊNH: Bạn cũng cần import LoginPage ở file root ===
    # (Trong file này không cần, nhưng file chạy app thì cần)

except ImportError as e:
    print(f"LỖI IMPORT TRANG CON: {e}")
    exit()

# --- Định nghĩa màu sắc (Dùng chung) ---
COLOR_SIDEBAR_BG = "#FFFFFF"
COLOR_MAIN_BG = "#F8F9FA"
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY_TEAL = "#00A79E"
COLOR_ACTIVE_BG = "#E0F7FA"
COLOR_ACTIVE_FG = "#00A79E"
COLOR_SIDEBAR_FG = "#333333"


class Application(ttk.Frame):
    def __init__(self, parent, style, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.style = style

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
        # SỬA: Đảm bảo tên trang 'DashbroadPage' ở đây khớp
        for F in (DashbroadPage, DriverPage, VehiclePage, CustomerPage, TripPage):
            page_name = F.__name__
            frame = F(self.content_frame, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("DashbroadPage")

    def setup_styles(self):
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

        ttk.Label(sidebar, text="Quản Lý",
                  font=("Arial", 22, "bold"),
                  foreground=COLOR_PRIMARY_TEAL,
                  background=COLOR_SIDEBAR_BG).pack(pady=30, padx=20)

        self.nav_buttons = {}
        nav_items = [
            # SỬA: Đảm bảo tên trang 'DashbroadPage' ở đây khớp
            ("DashbroadPage", "Tổng Quan"),
            ("DriverPage", "Quản Lý Tài Xế"),
            ("VehiclePage", "Quản Lý Phương Tiện"),
            ("CustomerPage", "Quản Lý Khách Hàng"),
            ("TripPage", "Quản Lý Chuyến Đi")
        ]

        for page_name, text in nav_items:
            btn = ttk.Button(sidebar, text=text, style='Sidebar.TButton',
                             command=lambda p=page_name: self.show_frame(p))
            btn.pack(fill="x", padx=20, pady=5)
            self.nav_buttons[page_name] = btn

        # === THÊM MỚI: NÚT ĐĂNG XUẤT ===
        # Đặt nút này ở cuối sidebar
        logout_button = ttk.Button(sidebar,
                                   text="Đăng Xuất",
                                   bootstyle="danger",  # Style màu đỏ
                                   command=self.handle_logout)
        logout_button.pack(side="bottom", fill="x", padx=20, pady=20)

        # Thêm đường kẻ ngang
        sep = ttk.Separator(sidebar)
        sep.pack(side="bottom", fill="x", padx=20)
        # === KẾT THÚC THÊM MỚI ===

        return sidebar

    # === THÊM MỚI: HÀM XỬ LÝ ĐĂNG XUẤT ===
    def handle_logout(self):
        """
        Xử lý đăng xuất.
        Hàm này gọi hàm 'show_frame' của 'parent' (cửa sổ chính)
        để hiển thị lại trang 'LoginPage'.
        """
        try:
            # self.parent là cửa sổ chính (root window)
            # Giả định root window có hàm show_frame()
            print("Đang đăng xuất... Chuyển về LoginPage.")
            self.parent.show_frame("LoginPage")
        except AttributeError:
            print("Lỗi: Không thể đăng xuất.")
            print("Hãy đảm bảo file app chính (root) của bạn có hàm 'show_frame('LoginPage')'.")
        except Exception as e:
            print(f"Lỗi khi đăng xuất: {e}")

    # === SỬA LẠI: HÀM SHOW_FRAME ===
    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if not frame:
            print(f"Lỗi: Không tìm thấy trang {page_name}")
            return

        # === THÊM VÀO: LÀM MỚI DỮ LIỆU KHI CHUYỂN TRANG ===
        # (Đây là mấu chốt để sửa lỗi 'Đang tải...')
        if hasattr(frame, 'refresh_data'):
            try:
                print(f"Đang làm mới trang: {page_name}")
                frame.refresh_data()
            except Exception as e:
                print(f"Lỗi khi làm mới {page_name}: {e}")
        # === KẾT THÚC THÊM ===

        frame.tkraise()

        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configure(style='Active.TButton')
            else:
                button.configure(style='Sidebar.TButton')