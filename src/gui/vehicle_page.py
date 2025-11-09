import tkinter as tk
from tkinter import font as tkfont
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# === IMPORT MỚI: TỪ MODEL ===
try:
    from models.vehicle_model import VehicleModel
except ImportError as e:
    print(f"Lỗi Import trong vehicle_page: {e}")

# Định nghĩa màu sắc (cần dùng cho các con số)
COLOR_PRIMARY_TEAL = "#00A79E"


class VehiclePage(ttk.Frame):
    """Trang Giao diện Quản lý Phương Tiện (Kết nối Database)"""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.configure(padding=(20, 10))

        # === KHỞI TẠO MODEL ===
        try:
            self.db_model = VehicleModel()
        except Exception as e:
            print(f"Không thể khởi tạo VehicleModel: {e}")
            self.db_model = None

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

        # (Code của 3 thẻ Card thống kê - Tạm thời giữ số liệu mẫu)
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

        # Các cột này PHẢI KHỚP với câu query SELECT
        columns = ("plate", "type", "driver_name", "mileage", "last_maintenance", "status")

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
        self.tree.heading("driver_name", text="Tài Xế Phụ Trách")
        self.tree.column("driver_name", width=200)
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

        # === SỬA LỖI Ở ĐÂY ===
        # Gán Label cho 'self.pagination_label'
        self.pagination_label = ttk.Label(pagination_frame, text="Đang tải...", style="secondary.TLabel")
        self.pagination_label.pack(side="left")
        # =======================

    def on_tab_selected(self, event):
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

    def load_data_into_tree(self, filter_status=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.db_model:
            ttk.Label(self, text="Lỗi: Không thể kết nối Model.", bootstyle="danger").pack()
            return

        try:
            vehicle_data = self.db_model.get_all_vehicles(status=filter_status)
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu phương tiện: {e}")
            vehicle_data = []

        tag_map = {
            "Hoạt động": "hoatdong",
            "Bảo trì": "baotri",
            "Ngừng hoạt động": "ngung"
        }

        count = 0
        for item in vehicle_data:
            data_values = item
            status_value = item[-1]
            status_tag = tag_map.get(status_value, "")
            self.tree.insert("", "end", text="", values=data_values, tags=(status_tag,))
            count += 1
        pagination_frame = ttk.Frame(self, style="TFrame")
        pagination_frame.pack(fill="x", pady=(10, 0))
        # Dòng này giờ sẽ chạy được
        ttk.Label(pagination_frame, text="Đang tải...", style="secondary.TLabel").pack(side="left")

    def on_tree_select(self, event):
        if self.tree.selection():
            self.edit_button.config(state="enabled")
            self.delete_button.config(state="enabled")
        else:
            self.edit_button.config(state="disabled")

    def deselect_tree(self, event):
        if not self.tree.identify_region(event.x, event.y) == "heading":
            if not self.tree.focus():
                self.tree.selection_set()