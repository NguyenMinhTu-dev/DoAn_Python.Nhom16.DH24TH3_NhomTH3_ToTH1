import customtkinter as ctk
import tkinter as tk
import subprocess
import sys
import os

# --- 1. Cấu hình & Màu sắc ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLOR_PRIMARY = "#20B2AA"
COLOR_BACKGROUND = "#F5F6F8"
COLOR_TEXT_DARK = "#29313D"
COLOR_WHITE = "#FFFFFF"
COLOR_GRAY_LIGHT = "#F0F0F0"
COLOR_GRAY_TEXT = "#6A707E"
COLOR_YELLOW = "#FCA311"
COLOR_GREEN_STATUS = "#16A34A"
COLOR_GRAY_STATUS = "#6B7280"
COLOR_YELLOW_STATUS = "#F59E0B"


# --- 2. Lớp ứng dụng chính (Quản lý các trang) ---
class MainWindowApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Xanh SM - Hệ thống Quản lý")
        self.geometry("1100x768")  # Tăng chiều rộng một chút
        self.minsize(900, 600)
        self.configure(fg_color=COLOR_BACKGROUND)

        # --- Cấu hình Grid Layout chính ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Khung Sidebar ---
        self.sidebar_frame = self._create_sidebar()
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")

        # --- Khung chứa nội dung chính (sẽ chứa các trang) ---
        self.main_content_frame = ctk.CTkFrame(self, fg_color=COLOR_BACKGROUND, corner_radius=0)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        self.pages = {}

        # Tạo các trang
        for Page in (DashboardPage, DriverPage):
            page_name = Page.__name__
            frame = Page(self.main_content_frame, self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Hiển thị trang Tổng Quan (Dashboard) đầu tiên
        self.show_page("DashboardPage")

    def _create_sidebar(self):
        """Tạo cột menu bên trái"""
        sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLOR_WHITE)
        sidebar_frame.grid_rowconfigure(7, weight=1)  # Đẩy nút đăng xuất xuống

        logo_label = ctk.CTkLabel(sidebar_frame, text="✔ XANH SM", font=ctk.CTkFont(size=18, weight="bold"),
                                  text_color=COLOR_PRIMARY)
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="w")

        # Các nút menu
        self.dashboard_button = self._create_menu_item(sidebar_frame, 1, "Tổng Quan",
                                                       lambda: self.show_page("DashboardPage"))
        self.driver_button = self._create_menu_item(sidebar_frame, 2, "Quản Lý Tài Xế",
                                                    lambda: self.show_page("DriverPage"))
        self._create_menu_item(sidebar_frame, 3, "Quản Lý Chuyến Đi", None)  # (Chưa có chức năng)
        self._create_menu_item(sidebar_frame, 4, "Quản Lý Khách Hàng", None)
        self._create_menu_item(sidebar_frame, 5, "Thống Kê", None)
        self._create_menu_item(sidebar_frame, 6, "Cài Đặt", None)

        # Nút Đăng Xuất
        logout_btn = ctk.CTkButton(sidebar_frame, text="← Đăng Xuất",
                                   command=self.logout,
                                   fg_color="transparent",
                                   hover_color=COLOR_BACKGROUND,
                                   text_color=COLOR_TEXT_DARK,
                                   font=ctk.CTkFont(size=13, weight="bold"),
                                   anchor="w")
        logout_btn.grid(row=8, column=0, padx=20, pady=(0, 20), sticky="s")

        return sidebar_frame

    def _create_menu_item(self, parent, row, text, command):
        """Hàm trợ giúp tạo nút menu sidebar"""
        item_frame = ctk.CTkFrame(parent, corner_radius=5, fg_color=COLOR_WHITE, height=40)
        item_frame.grid(row=row, column=0, sticky="ew", padx=10, pady=2)

        btn = ctk.CTkButton(item_frame, text=text, font=ctk.CTkFont(size=13),
                            text_color=COLOR_TEXT_DARK,
                            fg_color="transparent",
                            hover_color=COLOR_BACKGROUND,
                            command=command,
                            anchor="w")
        btn.pack(padx=20, pady=5, fill="x")
        return btn

    def show_page(self, page_name):
        """Hiển thị một trang và cập nhật trạng thái active của menu"""
        # Cập nhật trạng thái active của nút menu
        self.dashboard_button.configure(fg_color=COLOR_BACKGROUND if page_name == "DashboardPage" else "transparent")
        self.driver_button.configure(fg_color=COLOR_BACKGROUND if page_name == "DriverPage" else "transparent")

        # Hiển thị trang
        frame = self.pages[page_name]
        frame.tkraise()

    def logout(self):
        """Mở lại cửa sổ đăng nhập và đóng cửa sổ hiện tại"""
        python_executable = sys.executable
        current_dir = os.path.dirname(os.path.abspath(__file__))
        login_file = os.path.join(current_dir, "Login.py")  # Giả sử tên là "Login.py"

        try:
            subprocess.Popen([python_executable, login_file])
            self.destroy()
        except FileNotFoundError:
            tk.messagebox.showerror("Lỗi", f"Không tìm thấy file Login.py tại:\n{login_file}")
        except Exception as e:
            tk.messagebox.showerror("Lỗi", f"Không thể mở lại Login.py: {e}")


# --- 3. Trang Tổng Quan (DashboardPage) ---
class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_BACKGROUND)
        self.controller = controller

        # Cấu hình grid
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Tiêu đề
        ctk.CTkLabel(self, text="Tổng Quan", font=ctk.CTkFont(size=20, weight="bold"), text_color=COLOR_TEXT_DARK).grid(
            row=0, column=0, columnspan=3, padx=30, pady=(20, 5), sticky="w")
        ctk.CTkLabel(self, text="Xem tổng quan về hoạt động của hệ thống.", font=ctk.CTkFont(size=12),
                     text_color=COLOR_GRAY_TEXT).grid(row=0, column=0, columnspan=3, padx=30, pady=(45, 10), sticky="w")

        # Hàng 1: Các thẻ thông tin
        self._create_info_card(0, "Tổng Doanh Thu", "123.456.789 đ", "+20.1%", COLOR_PRIMARY).grid(row=1, column=0,
                                                                                                   padx=(30, 15),
                                                                                                   pady=20,
                                                                                                   sticky="nsew")
        self._create_info_card(1, "Tổng Số Khách Hàng", "1.234", "+380", COLOR_YELLOW).grid(row=1, column=1, padx=15,
                                                                                            pady=20, sticky="nsew")
        self._create_info_card(2, "Tổng Số Tài Xế", "573", "+24", COLOR_PRIMARY).grid(row=1, column=2, padx=(15, 30),
                                                                                      pady=20, sticky="nsew")

        # Hàng 2: Biểu đồ và Giao dịch
        self._create_chart_mockup().grid(row=2, column=0, columnspan=2, padx=(30, 15), pady=(0, 30), sticky="nsew")
        self._create_trips_list().grid(row=2, column=2, padx=(15, 30), pady=(0, 30), sticky="nsew")

    def _create_info_card(self, col, title, value, detail, color):
        card = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=10, height=120)
        card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(card, text="□", font=ctk.CTkFont(size=20, weight="bold"), text_color=color).grid(row=0, column=1,
                                                                                                      padx=15, pady=10,
                                                                                                      sticky="e")
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), text_color=COLOR_GRAY_TEXT).grid(row=0, column=0,
                                                                                                   padx=15,
                                                                                                   pady=(10, 5),
                                                                                                   sticky="w")
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_TEXT_DARK).grid(row=1,
                                                                                                                  column=0,
                                                                                                                  padx=15,
                                                                                                                  pady=(
                                                                                                                      0,
                                                                                                                      5),
                                                                                                                  sticky="w")
        ctk.CTkLabel(card, text=detail, font=ctk.CTkFont(size=10), text_color=color).grid(row=2, column=0, padx=15,
                                                                                          pady=(0, 10), sticky="w")
        return card

    def _create_chart_mockup(self):
        chart_frame = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=10)
        chart_frame.grid_columnconfigure(0, weight=1)
        chart_frame.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(chart_frame, text="Tổng Quan", font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=COLOR_TEXT_DARK).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        bar_container = ctk.CTkFrame(chart_frame, fg_color=COLOR_WHITE)
        bar_container.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        data_heights = [0.2, 0.3, 0.4, 0.45, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
        labels = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"]
        for i, (h, label) in enumerate(zip(data_heights, labels)):
            bar_container.grid_columnconfigure(i, weight=1)
            col_frame = ctk.CTkFrame(bar_container, fg_color="transparent")
            col_frame.grid(row=0, column=i, sticky="ns", padx=4)
            col_frame.grid_rowconfigure(0, weight=int((1 - h) * 100))
            col_frame.grid_rowconfigure(1, weight=int(h * 100))
            bar = ctk.CTkFrame(col_frame, fg_color=COLOR_PRIMARY, corner_radius=3)
            bar.grid(row=1, column=0, sticky="nsew")
            ctk.CTkLabel(bar_container, text=label, font=ctk.CTkFont(size=10), text_color=COLOR_GRAY_TEXT).grid(row=1,
                                                                                                                column=i,
                                                                                                                sticky="n",
                                                                                                                pady=(5,
                                                                                                                      0))
        return chart_frame

    def _create_trips_list(self):
        trip_frame = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=10)
        trip_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(trip_frame, text="Chuyến Đi Gần Đây", font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=COLOR_TEXT_DARK).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")
        trip_data = [("Nguyễn Văn A", "Q.1 → Q.7", "150.000 đ"), ("Trần Thị B", "Q.Bình Thạnh → Q.3", "120.000 đ"),
                     ("Lê Văn C", "Q.Gò Vấp → P.Nhuận", "180.000 đ"), ("Phạm Thị D", "Q.Tân Bình → Q.10", "95.000 đ"),
                     ("Hoàng Văn E", "Q.2 → Q.4", "135.000 đ")]
        for i, (name, route, price) in enumerate(trip_data):
            self._create_trip_item(trip_frame, i + 1, name, route, price)
        return trip_frame

    def _create_trip_item(self, parent, row, name, route, price):
        ctk.CTkLabel(parent, text=name, font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT_DARK).grid(
            row=row, column=0, padx=(20, 10), pady=(5, 0), sticky="w")
        ctk.CTkLabel(parent, text=route, font=ctk.CTkFont(size=11), text_color=COLOR_GRAY_TEXT).grid(row=row + 1,
                                                                                                     column=0,
                                                                                                     padx=(20, 10),
                                                                                                     pady=(0, 5),
                                                                                                     sticky="w")
        ctk.CTkLabel(parent, text=price, font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT_DARK).grid(
            row=row, column=1, rowspan=2, padx=(10, 20), sticky="e")
        if row < 10:
            sep = ctk.CTkFrame(parent, height=1, fg_color=COLOR_BACKGROUND)
            sep.grid(row=row + 2, column=0, columnspan=2, sticky="ew", padx=20, pady=(5, 0))


# --- 4. Trang Quản Lý Tài Xế (DriverPage) ---
class DriverPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_BACKGROUND)
        self.controller = controller

        # Cấu hình grid
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(2, weight=1)  # Dòng cho table

        # Tiêu đề & Nút Thêm
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=3, padx=30, pady=(20, 5), sticky="ew")
        ctk.CTkLabel(header_frame, text="Quản Lý Tài Xế", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=COLOR_TEXT_DARK).pack(side="left")
        ctk.CTkButton(header_frame, text="+ Thêm Tài Xế", fg_color=COLOR_PRIMARY, hover_color="#1A9E96").pack(
            side="right")

        # Hàng 1: Các thẻ thông tin
        self._create_info_card(0, "Tổng Số Tài Xế", "573", "+24 tài xế mới", COLOR_PRIMARY).grid(row=1, column=0,
                                                                                                 padx=(30, 15), pady=20,
                                                                                                 sticky="nsew")
        self._create_info_card(1, "Tài Xế Hoạt Động", "498", "86.9% tổng số", COLOR_GREEN_STATUS).grid(row=1, column=1,
                                                                                                       padx=15, pady=20,
                                                                                                       sticky="nsew")
        self._create_info_card(2, "Tài Xế Không Hoạt Động", "75", "13.1% tổng số", COLOR_GRAY_STATUS).grid(row=1,
                                                                                                           column=2,
                                                                                                           padx=(15,
                                                                                                                 30),
                                                                                                           pady=20,
                                                                                                           sticky="nsew")

        # Hàng 2: Khu vực Bảng (Table)
        self._create_table_area().grid(row=2, column=0, columnspan=3, padx=(30, 30), pady=(0, 30), sticky="nsew")

    def _create_info_card(self, col, title, value, detail, color):
        # Tái sử dụng hàm từ DashboardPage
        card = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=10, height=120)
        card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(card, text="□", font=ctk.CTkFont(size=20, weight="bold"), text_color=color).grid(row=0, column=1,
                                                                                                      padx=15, pady=10,
                                                                                                      sticky="e")
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), text_color=COLOR_GRAY_TEXT).grid(row=0, column=0,
                                                                                                   padx=15,
                                                                                                   pady=(10, 5),
                                                                                                   sticky="w")
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_TEXT_DARK).grid(row=1,
                                                                                                                  column=0,
                                                                                                                  padx=15,
                                                                                                                  pady=(
                                                                                                                      0,
                                                                                                                      5),
                                                                                                                  sticky="w")
        ctk.CTkLabel(card, text=detail, font=ctk.CTkFont(size=10), text_color=color).grid(row=2, column=0, padx=15,
                                                                                          pady=(0, 10), sticky="w")
        return card

    def _create_table_area(self):
        """Tạo khu vực chứa tabs và bảng dữ liệu"""
        table_container = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=10)
        table_container.grid_rowconfigure(1, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # Tạo Tab view
        tab_view = ctk.CTkTabview(table_container, fg_color="transparent", text_color=COLOR_TEXT_DARK)
        tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        tabs = ["Tất Cả", "Đang Hoạt Động", "Tạm Ngưng", "Chờ Duyệt"]
        for tab_name in tabs:
            tab = tab_view.add(tab_name)
            self._populate_driver_tab(tab, tab_name)  # Điền nội dung cho tab

        return table_container

    def _populate_driver_tab(self, tab, tab_name):
        """Điền nội dung mô phỏng cho mỗi tab"""
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # Khung tìm kiếm (Mô phỏng)
        search_frame = ctk.CTkFrame(tab, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkEntry(search_frame, placeholder_text="Tìm Mã Tài Xế, Tên, SĐT...").pack(side="left", fill="x",
                                                                                       expand=True, padx=(0, 10))
        ctk.CTkButton(search_frame, text="Tìm kiếm nâng cao", fg_color="transparent", border_width=1,
                      text_color=COLOR_TEXT_DARK).pack(side="left", padx=10)
        ctk.CTkButton(search_frame, text="+ Thêm Tài Xế", fg_color=COLOR_PRIMARY, hover_color="#1A9E96").pack(
            side="left")

        # Khung có thể cuộn chứa bảng
        scrollable_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # --- Tạo Bảng (Mô phỏng bằng Grid) ---
        table_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        table_frame.grid(row=0, column=0, sticky="ew")

        # Định nghĩa các cột (tỷ lệ weight)
        columns = {
            0: (ctk.CTkCheckBox(table_frame, text="", width=20), 0),  # Checkbox
            1: (ctk.CTkLabel(table_frame, text="Mã Tài Xế", font=ctk.CTkFont(weight="bold")), 1),
            2: (ctk.CTkLabel(table_frame, text="Họ Tên", font=ctk.CTkFont(weight="bold")), 2),
            3: (ctk.CTkLabel(table_frame, text="Loại Xe", font=ctk.CTkFont(weight="bold")), 1),
            4: (ctk.CTkLabel(table_frame, text="SĐT", font=ctk.CTkFont(weight="bold")), 2),
            5: (ctk.CTkLabel(table_frame, text="Đánh Giá", font=ctk.CTkFont(weight="bold")), 1),
            6: (ctk.CTkLabel(table_frame, text="Trạng Thái", font=ctk.CTkFont(weight="bold")), 1),
            7: (ctk.CTkLabel(table_frame, text="...", font=ctk.CTkFont(weight="bold")), 0)  # Nút ...
        }

        # Tạo Header
        for col, (widget, weight) in columns.items():
            table_frame.grid_columnconfigure(col, weight=weight)
            widget.grid(row=0, column=col, padx=10, pady=10, sticky="w")

        # Đường kẻ ngang
        ctk.CTkFrame(table_frame, height=1, fg_color=COLOR_GRAY_LIGHT).grid(row=1, column=0, columnspan=8, sticky="ew")

        # Dữ liệu mẫu
        driver_data = [
            ("TX001", "Nguyễn Văn An", "Xe 4 Chỗ", "0901234567", "4.8 ★", "Hoạt động"),
            ("TX002", "Trần Văn Bình", "Xe 7 Chỗ", "0912345678", "4.5 ★", "Hoạt động"),
            ("TX003", "Lê Thị Cẩm", "Xe 4 Chỗ", "0923456789", "4.2 ★", "Tạm ngưng"),
            ("TX004", "Phạm Văn Dũng", "Xe 4 Chỗ", "0934567890", "4.9 ★", "Hoạt động"),
            ("TX005", "Hoàng Thị Em", "Xe 4 Chỗ", "0945678901", "---", "Chờ duyệt"),
            ("TX006", "Vũ Văn Phúc", "Xe 7 Chỗ", "0956789012", "4.6 ★", "Hoạt động"),
            ("TX007", "Đặng Thị Giang", "Xe 4 Chỗ", "0967890123", "3.9 ★", "Tạm ngưng"),
            ("TX008", "Bùi Văn Hùng", "Xe 7 Chỗ", "0978901234", "4.7 ★", "Hoạt động"),
        ]

        # Chỉ hiển thị dữ liệu phù hợp với tab (Mô phỏng)
        filtered_data = []
        if tab_name == "Tất Cả":
            filtered_data = driver_data
        elif tab_name == "Đang Hoạt Động":
            filtered_data = [d for d in driver_data if d[5] == "Hoạt động"]
        elif tab_name == "Tạm Ngưng":
            filtered_data = [d for d in driver_data if d[5] == "Tạm ngưng"]
        elif tab_name == "Chờ Duyệt":
            filtered_data = [d for d in driver_data if d[5] == "Chờ duyệt"]

        # Tạo các hàng dữ liệu
        for i, data in enumerate(filtered_data):
            row_index = i + 2  # (0 là header, 1 là đường kẻ)

            # Checkbox
            ctk.CTkCheckBox(table_frame, text="", width=20).grid(row=row_index, column=0, padx=10, pady=5, sticky="w")

            # Dữ liệu (Mã, Tên, Loại Xe, SĐT, Đánh Giá)
            ctk.CTkLabel(table_frame, text=data[0]).grid(row=row_index, column=1, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(table_frame, text=data[1], anchor="w").grid(row=row_index, column=2, padx=10, pady=5,
                                                                     sticky="ew")
            ctk.CTkLabel(table_frame, text=data[2]).grid(row=row_index, column=3, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(table_frame, text=data[3]).grid(row=row_index, column=4, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(table_frame, text=data[4]).grid(row=row_index, column=5, padx=10, pady=5, sticky="w")

            # Trạng thái (Badge)
            status = data[5]
            if status == "Hoạt động":
                color = COLOR_GREEN_STATUS
            elif status == "Tạm ngưng":
                color = COLOR_GRAY_STATUS
            else:
                color = COLOR_YELLOW_STATUS

            ctk.CTkLabel(table_frame, text=status, fg_color=color, text_color=COLOR_WHITE, corner_radius=10,
                         font=ctk.CTkFont(size=10)).grid(row=row_index, column=6, padx=10, pady=5, sticky="w")

            # Nút ...
            ctk.CTkButton(table_frame, text="...", width=20, fg_color="transparent", text_color=COLOR_TEXT_DARK).grid(
                row=row_index, column=7, padx=10, pady=5, sticky="w")

            # Đường kẻ
            ctk.CTkFrame(table_frame, height=1, fg_color=COLOR_GRAY_LIGHT).grid(row=row_index + 1, column=0,
                                                                                columnspan=8, sticky="ew")

        # --- Pagination (Mô phỏng) ---
        pagination_frame = ctk.CTkFrame(tab, fg_color="transparent")
        pagination_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(pagination_frame, text=f"0 trong {len(filtered_data)} hàng được chọn",
                     text_color=COLOR_GRAY_TEXT).pack(side="left", padx=10)
        ctk.CTkLabel(pagination_frame, text="Trang 1/1", text_color=COLOR_GRAY_TEXT).pack(side="right", padx=10)


if __name__ == "__main__":
    app = MainWindowApp()
    app.mainloop()