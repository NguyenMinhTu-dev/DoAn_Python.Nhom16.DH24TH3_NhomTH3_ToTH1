import tkinter as tk
from tkinter import font as tkfont
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from driver_page import DriverPage
from vehicle_page import VehiclePage
from customer_page import CustomerPage
# Import thư viện Matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- ĐỊNH NGHĨA MÀU SẮC (ĐÃ CẬP NHẬT) ---
COLOR_SIDEBAR_BG = "#FFFFFF"  # ĐỔI THÀNH MÀU TRẮNG
COLOR_MAIN_BG = "#F8F9FA"
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY_TEAL = "#00A79E"
COLOR_ACTIVE_BG = "#E0F7FA"
COLOR_ACTIVE_FG = "#00A79E"
COLOR_SIDEBAR_FG = "#333333"  # ĐỔI MÀU CHỮ SIDEBAR THÀNH ĐEN


# --- LỚP TRANG TỔNG QUAN (DASHBOARD) ---
class DashbroadPage(ttk.Frame):
    """Trang Dashboard chi tiết với các thẻ thống kê và biểu đồ"""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.configure(padding=20)

        # --- 1. Tiêu đề chính của Trang ---
        title_frame = ttk.Frame(self, style="TFrame")
        title_frame.pack(fill="x", anchor="n")
        ttk.Label(title_frame, text="Tổng Quan",
                  font=("Arial", 24, "bold"),
                  style="TLabel").pack(anchor="w")
        ttk.Label(title_frame, text="Xem tổng quan về hoạt động của hệ thống.",
                  style="secondary.TLabel").pack(anchor="w")

        # --- 2. Hàng 1: Các Thẻ Thống Kê ---
        stat_frame = ttk.Frame(self, style="TFrame")
        stat_frame.pack(fill="x", expand=True, pady=15)

        # Thẻ 1: Doanh Thu
        card1 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(card1, text="Tổng Doanh Thu", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card1, text="123.456.789 đ", font=("Arial", 22, "bold"), style="light.TLabel").pack(anchor="w",
                                                                                                      pady=5)
        ttk.Label(card1, text="+20.1% so với tháng trước", bootstyle="success").pack(anchor="w")

        # Thẻ 2: Khách Hàng
        card2 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card2.pack(side="left", fill="x", expand=True, padx=10)
        ttk.Label(card2, text="Tổng Số Khách Hàng", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card2, text="1.234", font=("Arial", 22, "bold"), style="light.TLabel").pack(anchor="w", pady=5)
        ttk.Label(card2, text="+160 khách hàng mới", bootstyle="info").pack(anchor="w")

        # Thẻ 3: Tài Xế
        card3 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card3.pack(side="left", fill="x", expand=True, padx=(10, 0))
        ttk.Label(card3, text="Tổng Số Tài Xế", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card3, text="573", font=("Arial", 22, "bold"), style="light.TLabel").pack(anchor="w", pady=5)
        ttk.Label(card3, text="+24 tài xế mới", bootstyle="info").pack(anchor="w")

        # --- 3. Hàng 2: Biểu đồ và Danh sách ---
        bottom_frame = ttk.Frame(self, style="TFrame")
        bottom_frame.pack(fill="both", expand=True, pady=10)

        bottom_frame.columnconfigure(0, weight=7)
        bottom_frame.columnconfigure(1, weight=3)
        bottom_frame.rowconfigure(0, weight=1)

        # Cột Trái: Biểu đồ
        chart_frame = ttk.Frame(bottom_frame, bootstyle="light", padding=20)
        chart_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.create_bar_chart(chart_frame)  # Gọi hàm vẽ biểu đồ

        # Cột Phải: Chuyến đi gần đây
        list_frame = ttk.Frame(bottom_frame, bootstyle="light", padding=20)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.create_recent_trips_list(list_frame)  # Gọi hàm tạo danh sách

    def create_bar_chart(self, parent):
        ttk.Label(parent, text="Tổng Quan",
                  font=("Arial", 16, "bold"), style="light.TLabel").pack(anchor="w")

        months = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']
        revenue = [100, 120, 150, 140, 160, 180, 200, 190, 210, 230, 240, 280]

        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(COLOR_CARD)

        ax = fig.add_subplot(111)
        ax.set_facecolor(COLOR_CARD)

        ax.bar(months, revenue, color=COLOR_PRIMARY_TEAL)

        ax.set_ylabel("Triệu (tr)")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#E0E0E0')
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.tick_params(axis='x', colors='#555')
        ax.tick_params(axis='y', colors='#555')

        ax.yaxis.grid(True, color='#E0E0E0', linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

    def create_recent_trips_list(self, parent):
        ttk.Label(parent, text="Chuyến Đi Gần Đây",
                  font=("Arial", 16, "bold"), style="light.TLabel").pack(anchor="w", pady=10)

        trips = [
            ("Nguyễn Văn A", "Q.1 -> Q.7", "150.000 đ"),
            ("Trần Thị B", "Q.Bình Thạnh -> Q.3", "120.000 đ"),
            ("Lê Văn C", "Q.Gò Vấp -> Q.Phú Nhuận", "180.000 đ"),
            ("Phạm Thị D", "Q.Tân Bình -> Q.10", "95.000 đ"),
            ("Hoàng Văn E", "Q.2 -> Q.4", "135.000 đ")
        ]

        for name, route, amount in trips:
            item_frame = ttk.Frame(parent, style="light.TFrame")
            item_frame.pack(fill="x", pady=8)

            info_frame = ttk.Frame(item_frame, style="light.TFrame")
            info_frame.pack(side="left", fill="x", expand=True, padx=10)

            ttk.Label(info_frame, text=name, font=("Arial", 11, "bold"), style="light.TLabel").pack(anchor="w")
            ttk.Label(info_frame, text=route, bootstyle="secondary").pack(anchor="w")

            ttk.Label(item_frame, text=amount, font=("Arial", 11, "bold"), style="light.TLabel").pack(side="right")

            ttk.Separator(parent).pack(fill="x")



# --- LỚP ỨNG DỤNG CHÍNH ---
class Application(ttk.Window):
    def __init__(self, *args, **kwargs):
        ttk.Window.__init__(self, *args, **kwargs)

        self.title("Hệ Thống Quản Lý")
        self.geometry("1400x800")
        self.configure(background=COLOR_MAIN_BG)

        self.setup_styles()

        self.sidebar_frame = self.create_sidebar()
        self.sidebar_frame.pack(side="left", fill="y")

        self.content_frame = ttk.Frame(self, bootstyle="light")
        self.content_frame.pack(side="right", fill="both", expand=True)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (DashbroadPage, DriverPage, VehiclePage,CustomerPage):
            page_name = F.__name__
            frame = F(self.content_frame, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("DashbroadPage")

    def setup_styles(self):
        style = Style.get_instance()

        # *** SỬA LỖI 2: ĐỔI SIDEBAR SANG TRẮNG ***
        style.configure('primary.TFrame', background=COLOR_SIDEBAR_BG)

        style.configure('TFrame', background=COLOR_MAIN_BG)
        style.configure('light.TFrame', background=COLOR_CARD)
        style.configure('TLabel', background=COLOR_MAIN_BG, foreground="#333")

        # *** SỬA LỖI 1: HIỂN THỊ CHỮ TRÊN CARD TRẮNG ***
        style.configure('light.TLabel', background=COLOR_CARD, foreground="#333333")

        sidebar_font = tkfont.Font(family="Arial", size=11, weight="bold")

        # Nút Thường (Nền trắng, chữ đen)
        style.configure('Sidebar.TButton',
                        font=sidebar_font,
                        foreground=COLOR_SIDEBAR_FG,  # Đã đổi thành #333
                        background=COLOR_SIDEBAR_BG,  # Đã đổi thành #FFFFFF
                        anchor="w",
                        padding=(15, 12),
                        borderwidth=0)
        style.map('Sidebar.TButton',
                  background=[('active', COLOR_ACTIVE_BG),  # Hover màu xanh nhạt
                              ('!active', COLOR_SIDEBAR_BG)])  # Nền trắng

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

        # Tiêu đề Sidebar (Chữ Xanh trên nền Trắng)
        ttk.Label(sidebar, text="XANH SM",
                  font=("Arial", 22, "bold"),
                  foreground=COLOR_PRIMARY_TEAL,
                  background=COLOR_SIDEBAR_BG).pack(pady=30, padx=20)

        self.nav_buttons = {}
        nav_items = [
            ("DashbroadPage", "Tổng Quan"),
            ("DriverPage", "Quản Lý Tài Xế"),
            ("VehiclePage", "Quản Lý Xe"),
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


# --- CHẠY ỨNG DỤNG ---
if __name__ == "__main__":
    app = Application(themename="cosmo")
    app.mainloop()