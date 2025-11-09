# vehicle_page.py
import tkinter as tk
from tkinter import font as tkfont
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# Định nghĩa màu sắc (cần dùng cho các con số)
COLOR_PRIMARY_TEAL = "#00A79E"


class VehiclePage(ttk.Frame):
    """Trang Giao diện Quản lý Phương Tiện (với Tabs Filter)"""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.configure(padding=(20, 10))

        # --- LƯU TRỮ DỮ LIỆU GỐC ---
        self.master_vehicle_data = [
            ("51F-123.45", "VinFast VF 8", "Nguyễn Văn A", "120.500 km", "10/10/2025", "Hoạt động", "hoatdong"),
            ("29A-987.65", "VinFast VF e34", "Trần Thị B", "85.000 km", "01/11/2025", "Hoạt động", "hoatdong"),
            ("92A-456.78", "VinFast VF 9", "Lê Văn C", "150.200 km", "15/09/2025", "Bảo trì", "baotri"),
            ("30E-333.33", "VinFast VF 5", "Phạm Thị D", "45.000 km", "20/10/2025", "Hoạt động", "hoatdong"),
            ("60C-555.55", "VinFast VF 8", "(Chưa gán)", "210.000 km", "01/01/2025", "Ngừng hoạt động", "ngung")
        ]

        # --- 1. Tiêu đề & Nút Thêm Mới ---
        title_frame = ttk.Frame(self, style="TFrame")
        title_frame.pack(fill="x", anchor="n", pady=(0, 10))

        left_title_frame = ttk.Frame(title_frame, style="TFrame")
        left_title_frame.pack(side="left", fill="x", expand=True)

        ttk.Label(left_title_frame, text="Quản Lý Phương Tiện",
                  font=("Arial", 24, "bold"),
                  style="TLabel").pack(anchor="w")
        ttk.Label(left_title_frame, text="Xem và quản lý thông tin phương tiện trong hệ thống.",
                  style="secondary.TLabel").pack(anchor="w")

        add_button = ttk.Button(title_frame, text="Thêm Xe Mới",
                                bootstyle="success")
        add_button.pack(side="right", anchor="ne", pady=10)

        # --- 2. Hàng Thống Kê ---
        stat_frame = ttk.Frame(self, style="TFrame")
        stat_frame.pack(fill="x", expand=True, pady=10)

        # (Code của 3 thẻ Card thống kê...)
        card1 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(card1, text="Tổng Số Phương Tiện", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card1, text="150", font=("Arial", 22, "bold"),
                  style="light.TLabel", foreground=COLOR_PRIMARY_TEAL).pack(anchor="w", pady=5)
        ttk.Label(card1, text="+5 xe mới trong tháng", bootstyle="success").pack(anchor="w")
        card2 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card2.pack(side="left", fill="x", expand=True, padx=10)
        ttk.Label(card2, text="Đang Hoạt Động", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card2, text="125", font=("Arial", 22, "bold"),
                  style="light.TLabel", foreground=COLOR_PRIMARY_TEAL).pack(anchor="w", pady=5)
        ttk.Label(card2, text="83.3% tổng số xe", bootstyle="info").pack(anchor="w")
        card3 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card3.pack(side="left", fill="x", expand=True, padx=(10, 0))
        ttk.Label(card3, text="Đang Bảo Trì", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card3, text="15", font=("Arial", 22, "bold"),
                  style="light.TLabel", foreground=COLOR_PRIMARY_TEAL).pack(anchor="w", pady=5)
        ttk.Label(card3, text="10% tổng số xe", bootstyle="warning").pack(anchor="w")

        # --- 3. Notebook (Tabs) ---
        notebook = ttk.Notebook(self)
        notebook.pack(fill="x", pady=10)

        tab_all = ttk.Frame(notebook)
        tab_active = ttk.Frame(notebook)
        tab_maintenance = ttk.Frame(notebook)
        tab_stopped = ttk.Frame(notebook)

        notebook.add(tab_all, text="  Tất Cả  ")
        notebook.add(tab_active, text="  Đang Hoạt Động  ")
        notebook.add(tab_maintenance, text="  Bảo Trì  ")
        notebook.add(tab_stopped, text="  Ngừng Hoạt Động  ")

        # === GÁN SỰ KIỆN KHI CHỌN TAB ===
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        # --- 4. Thanh hành động (Sửa, Xóa, Tìm kiếm) ---
        action_bar = ttk.Frame(self, style="TFrame")
        action_bar.pack(fill="x", pady=5)

        self.edit_button = ttk.Button(action_bar, text="Sửa",
                                      bootstyle="outline-warning",
                                      state="disabled")
        self.edit_button.pack(side="left", padx=(0, 5))

        self.delete_button = ttk.Button(action_bar, text="Xóa",
                                        bootstyle="outline-danger",
                                        state="disabled")
        self.delete_button.pack(side="left", padx=5)

        search_entry = ttk.Entry(action_bar, width=50)
        search_entry.pack(side="right", fill="x", expand=True)
        search_entry.insert(0, "Tìm theo biển số xe, loại xe...")

        # --- 5. Bảng Dữ Liệu (Treeview) ---
        table_container = ttk.Frame(self, style="TFrame")
        table_container.pack(fill="both", expand=True, pady=10)

        columns = ("plate", "type", "driver", "mileage", "last_maintenance", "status")

        self.tree = ttk.Treeview(table_container,
                                 columns=columns,
                                 show='tree headings',
                                 height=15)

        self.tree.heading("#0", text=" ")
        self.tree.column("#0", width=50, anchor="center")

        self.tree.heading("plate", text="Biển Số Xe")
        self.tree.column("plate", width=120, anchor="center")
        self.tree.heading("type", text="Loại Xe")
        self.tree.column("type", width=150)
        self.tree.heading("driver", text="Tài Xế Phụ Trách")
        self.tree.column("driver", width=200)
        self.tree.heading("mileage", text="Số Km")
        self.tree.column("mileage", width=100, anchor="e")
        self.tree.heading("last_maintenance", text="Bảo Trì Lần Cuối")
        self.tree.column("last_maintenance", width=150, anchor="center")
        self.tree.heading("status", text="Trạng Thái")
        self.tree.column("status", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure('hoatdong', foreground='#28a745')
        self.tree.tag_configure('baotri', foreground='#fd7e14')
        self.tree.tag_configure('ngung', foreground='#dc3545')

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.bind("<Button-1>", self.deselect_tree)
        action_bar.bind("<Button-1>", self.deselect_tree)

        # --- 6. Tải dữ liệu lần đầu (Tất Cả) ---
        self.load_data_into_tree(filter_status=None)

        # --- 7. Phân trang (Pagination) ---
        pagination_frame = ttk.Frame(self, style="TFrame")
        pagination_frame.pack(fill="x", pady=(10, 0))
        ttk.Label(pagination_frame, text="Hiển thị 1 - 5 trong 5", style="secondary.TLabel").pack(side="left")

    # --- HÀM MỚI: XỬ LÝ KHI CHỌN TAB ---
    def on_tab_selected(self, event):
        """Được gọi khi người dùng nhấp vào một tab"""
        selected_tab_text = event.widget.tab(event.widget.select(), "text").strip()

        self.tree.selection_set()

        if selected_tab_text == "Tất Cả":
            self.load_data_into_tree(filter_status=None)
        elif selected_tab_text == "Đang Hoạt Động":
            self.load_data_into_tree(filter_status="Hoạt động")
        elif selected_tab_text == "Bảo Trì":
            self.load_data_into_tree(filter_status="Bảo trì")
        elif selected_tab_text == "Ngừng Hoạt Động":
            self.load_data_into_tree(filter_status="Ngừng hoạt động")

    # --- HÀM MỚI: TẢI DỮ LIỆU CÓ LỌC ---
    def load_data_into_tree(self, filter_status=None):
        """Xóa bảng và tải lại dữ liệu dựa trên trạng thái lọc"""

        for item in self.tree.get_children():
            self.tree.delete(item)

        for item in self.master_vehicle_data:
            status_tag = item[-1]
            data_values = item[:-1]
            status_value = data_values[5]  # Vị trí cột 'status'

            if filter_status is None or status_value == filter_status:
                self.tree.insert("", "end", text="", values=data_values, tags=(status_tag,))

    def on_tree_select(self, event):
        """Kích hoạt nút Sửa/Xóa khi một dòng được chọn."""
        if self.tree.selection():
            self.edit_button.config(state="enabled")
            self.delete_button.config(state="enabled")
        else:
            self.edit_button.config(state="disabled")

    def deselect_tree(self, event):
        """Bỏ chọn tất cả các dòng khi nhấp ra ngoài."""
        if not self.tree.identify_region(event.x, event.y) == "heading":
            if not self.tree.focus():
                self.tree.selection_set()