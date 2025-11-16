import tkinter as tk
from tkinter import font as tkfont
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# Import thư viện Matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Định nghĩa màu sắc (cần dùng cho Matplotlib) ---
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY_TEAL = "#00A79E"
COLOR_MAIN_BG = "#F8F9FA"


class DashbroadPage(ttk.Frame):
    """Trang Dashboard chi tiết với các thẻ thống kê và biểu đồ"""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.configure(padding=20)

        # --- 1. Tiêu đề chính của Trang ---
        title_frame = ttk.Frame(self, style="TFrame")  # Style TFrame (nền xám nhạt)
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
        ttk.Label(card1, text="705.000 đ", font=("Arial", 22, "bold"), style="light.TLabel").pack(anchor="w",
                                                                                                      pady=5)
        ttk.Label(card1, text="+20.1% so với tháng trước", bootstyle="success").pack(anchor="w")

        # Thẻ 2: Khách Hàng
        card2 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card2.pack(side="left", fill="x", expand=True, padx=10)
        ttk.Label(card2, text="Tổng Số Khách Hàng", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card2, text="9", font=("Arial", 22, "bold"), style="light.TLabel").pack(anchor="w", pady=5)
        ttk.Label(card2, text="+3 khách hàng mới", bootstyle="info").pack(anchor="w")

        # Thẻ 3: Tài Xế
        card3 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card3.pack(side="left", fill="x", expand=True, padx=(10, 0))
        ttk.Label(card3, text="Tổng Số Tài Xế", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card3, text="7", font=("Arial", 22, "bold"), style="light.TLabel").pack(anchor="w", pady=5)
        ttk.Label(card3, text="+2 tài xế mới", bootstyle="info").pack(anchor="w")

        # --- 3. Hàng 2: Biểu đồ và Danh sách ---
        bottom_frame = ttk.Frame(self, style="TFrame")
        bottom_frame.pack(fill="both", expand=True, pady=10)

        # Cấu hình Grid cho 2 cột (Biểu đồ 70%, Danh sách 30%)
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
        """Tạo và nhúng biểu đồ cột Matplotlib vào 'parent'"""
        ttk.Label(parent, text="Tổng Quan",
                  font=("Arial", 16, "bold"), style="light.TLabel").pack(anchor="w")

        # Dữ liệu mẫu
        months = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']
        revenue = [100, 120, 150, 140, 160, 180, 200, 190, 210, 230, 240, 280]

        # Tạo Figure và Axes của Matplotlib
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(COLOR_CARD)  # Nền Figure màu trắng

        ax = fig.add_subplot(111)
        ax.set_facecolor(COLOR_CARD)  # Nền Axes màu trắng

        # Vẽ biểu đồ
        ax.bar(months, revenue, color=COLOR_PRIMARY_TEAL)

        # Tùy chỉnh giao diện (giống ảnh mẫu)
        ax.set_ylabel("Triệu (tr)")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#E0E0E0')
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.tick_params(axis='x', colors='#555')
        ax.tick_params(axis='y', colors='#555')

        # Thêm đường grid y
        ax.yaxis.grid(True, color='#E0E0E0', linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)  # Đưa grid ra sau

        fig.tight_layout()  # Tối ưu bố cục

        # Nhúng biểu đồ vào Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

    def create_recent_trips_list(self, parent):
        """Tạo danh sách các chuyến đi gần đây"""
        ttk.Label(parent, text="Chuyến Đi Gần Đây",
                  font=("Arial", 16, "bold"), style="light.TLabel").pack(anchor="w", pady=10)

        # Dữ liệu mẫu
        trips = [
            ("Nguyễn Văn A", "Q.1 -> Q.7", "150.000 đ"),
            ("Trần Thị B", "Q.Bình Thạnh -> Q.3", "120.000 đ"),
            ("Lê Văn C", "Q.Gò Vấp -> Q.Phú Nhuận", "180.000 đ"),
            ("Phạm Thị D", "Q.Tân Bình -> Q.10", "95.000 đ"),
            ("Hoàng Văn E", "Q.2 -> Q.4", "135.000 đ")
        ]

        for name, route, amount in trips:
            item_frame = ttk.Frame(parent, style="light.TFrame")  # Nền trắng
            item_frame.pack(fill="x", pady=8)

            # TODO: Thêm icon hình tròn

            info_frame = ttk.Frame(item_frame, style="light.TFrame")
            info_frame.pack(side="left", fill="x", expand=True, padx=10)

            ttk.Label(info_frame, text=name, font=("Arial", 11, "bold"), style="light.TLabel").pack(anchor="w")
            ttk.Label(info_frame, text=route, bootstyle="secondary").pack(anchor="w")

            ttk.Label(item_frame, text=amount, font=("Arial", 11, "bold"), style="light.TLabel").pack(side="right")

            ttk.Separator(parent).pack(fill="x")