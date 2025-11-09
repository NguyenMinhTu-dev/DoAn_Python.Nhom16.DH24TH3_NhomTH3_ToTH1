# customer_page.py
import tkinter as tk
from tkinter import font as tkfont
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# === IMPORT MỚI: TỪ MODEL ===
try:
    from models.customer_model import CustomerModel
except ImportError as e:
    print(f"Lỗi Import trong customer_page: {e}")

# Định nghĩa màu sắc (cần dùng cho các con số)
COLOR_PRIMARY_TEAL = "#00A79E"


class CustomerPage(ttk.Frame):
    """Trang Giao diện Quản lý Khách Hàng (Kết nối Database)"""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.configure(padding=(20, 10))

        # === KHỞI TẠO MODEL ===
        try:
            self.db_model = CustomerModel()
        except Exception as e:
            print(f"Không thể khởi tạo CustomerModel: {e}")
            self.db_model = None

        # --- XÓA DỮ LIỆU MẪU (master_customer_data) ---
        # (self.master_customer_data đã bị xóa)

        # --- 1. Tiêu đề & Nút Thêm Mới ---
        title_frame = ttk.Frame(self, style="TFrame")
        title_frame.pack(fill="x", anchor="n", pady=(0, 10))

        left_title_frame = ttk.Frame(title_frame, style="TFrame")
        left_title_frame.pack(side="left", fill="x", expand=True)

        ttk.Label(left_title_frame, text="Quản Lý Khách Hàng",
                  font=("Arial", 24, "bold"),
                  style="TLabel").pack(anchor="w")
        ttk.Label(left_title_frame, text="Xem và quản lý thông tin khách hàng trong hệ thống.",
                  style="secondary.TLabel").pack(anchor="w")

        add_button = ttk.Button(title_frame, text="Thêm Khách Hàng",
                                bootstyle="success")
        add_button.pack(side="right", anchor="ne", pady=10)

        # --- 2. Hàng Thống Kê ---
        stat_frame = ttk.Frame(self, style="TFrame")
        stat_frame.pack(fill="x", expand=True, pady=10)

        # (Code của 3 thẻ Card thống kê - Tạm thời giữ số liệu mẫu)
        card1 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(card1, text="Tổng Số Khách Hàng", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card1, text="1.234", font=("Arial", 22, "bold"),
                  style="light.TLabel", foreground=COLOR_PRIMARY_TEAL).pack(anchor="w", pady=5)
        ttk.Label(card1, text="+160 khách mới tháng này", bootstyle="success").pack(anchor="w")
        card2 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card2.pack(side="left", fill="x", expand=True, padx=10)
        ttk.Label(card2, text="Khách Hàng VIP", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card2, text="50", font=("Arial", 22, "bold"),
                  style="light.TLabel", foreground=COLOR_PRIMARY_TEAL).pack(anchor="w", pady=5)
        ttk.Label(card2, text="Chiếm 4.0% tổng số", bootstyle="info").pack(anchor="w")
        card3 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card3.pack(side="left", fill="x", expand=True, padx=(10, 0))
        ttk.Label(card3, text="Khách Hàng Bạc", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card3, text="300", font=("Arial", 22, "bold"),
                  style="light.TLabel", foreground=COLOR_PRIMARY_TEAL).pack(anchor="w", pady=5)
        ttk.Label(card3, text="Chiếm 24.3% tổng số", bootstyle="info").pack(anchor="w")

        # --- 3. Notebook (Tabs) ---
        notebook = ttk.Notebook(self)
        notebook.pack(fill="x", pady=10)

        tab_all = ttk.Frame(notebook)
        tab_vip = ttk.Frame(notebook)
        tab_silver = ttk.Frame(notebook)
        tab_bronze = ttk.Frame(notebook)

        notebook.add(tab_all, text="  Tất Cả  ")
        notebook.add(tab_vip, text="  VIP  ")
        notebook.add(tab_silver, text="  Bạc  ")
        notebook.add(tab_bronze, text="  Đồng  ")

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
        search_entry.insert(0, "Tìm theo mã KH, tên, SĐT...")

        # --- 5. Bảng Dữ Liệu (Treeview) ---
        table_container = ttk.Frame(self, style="TFrame")
        table_container.pack(fill="both", expand=True, pady=10)

        # SỬA: Bỏ cột 'trips' (tổng chuyến đi)
        columns = ("id", "name", "phone", "email", "rank")

        self.tree = ttk.Treeview(table_container,
                                 columns=columns,
                                 show='tree headings',
                                 height=15)

        self.tree.heading("#0", text=" ")
        self.tree.column("#0", width=50, anchor="center")

        self.tree.heading("id", text="Mã Khách Hàng")
        self.tree.column("id", width=100, anchor="center")
        self.tree.heading("name", text="Họ Tên")
        self.tree.column("name", width=250)
        self.tree.heading("phone", text="Số Điện Thoại")
        self.tree.column("phone", width=120, anchor="center")
        self.tree.heading("email", text="Email")
        self.tree.column("email", width=250)
        # SỬA: Xóa cột 'trips'
        self.tree.heading("rank", text="Hạng")
        self.tree.column("rank", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Cấu hình Tags (Tạo màu cho Hạng)
        self.tree.tag_configure('vip', foreground='#fd7e14')  # Cam
        self.tree.tag_configure('bac', foreground='#6c757d')  # Xám
        self.tree.tag_configure('dong', foreground='#17a2b8')  # Xanh lơ

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
        """Được gọi khi người dùng nhấp vào một tab"""
        selected_tab_text = event.widget.tab(event.widget.select(), "text").strip()
        self.tree.selection_set()

        # Truyền giá trị Tiếng Việt của CSDL
        if selected_tab_text == "Tất Cả":
            self.load_data_into_tree(filter_status=None)
        elif selected_tab_text == "VIP":
            self.load_data_into_tree(filter_status="VIP")
        elif selected_tab_text == "Bạc":
            self.load_data_into_tree(filter_status="Bạc")
        elif selected_tab_text == "Đồng":
            self.load_data_into_tree(filter_status="Đồng")

    def load_data_into_tree(self, filter_status=None):
        """Xóa bảng và tải lại dữ liệu dựa trên trạng thái lọc"""

        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.db_model:
            ttk.Label(self, text="Lỗi: Không thể kết nối Model.", bootstyle="danger").pack()
            return

        try:
            # === LẤY DỮ LIỆU TỪ DATABASE ===
            customer_data = self.db_model.get_all_customers(rank=filter_status)
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu khách hàng: {e}")
            customer_data = []

        # Tạo map (ánh xạ) từ giá trị trạng thái sang tag
        tag_map = {
            "VIP": "vip",
            "Bạc": "bac",
            "Đồng": "dong"
        }

        # Lặp qua DỮ LIỆU TỪ DB và thêm vào bảng
        count = 0
        for item in customer_data:
            # item là một tuple, vd: ('KH001', 'Nguyễn Thị An', ...)
            data_values = item

            # Lấy giá trị hạng (cột cuối cùng)
            status_value = item[-1]
            # Lấy tag màu tương ứng
            status_tag = tag_map.get(status_value, "")

            self.tree.insert("", "end", text="", values=data_values, tags=(status_tag,))
            count += 1

        pagination_frame = ttk.Frame(self, style="TFrame")
        pagination_frame.pack(fill="x", pady=(10, 0))
        # Dòng này giờ sẽ chạy được
        ttk.Label(pagination_frame, text="Đang tải...", style="secondary.TLabel").pack(side="left")

    def on_tree_select(self, event):
        """Kích hoạt nút Sửa/Xóa khi một dòng được chọn."""
        if self.tree.selection():
            self.edit_button.config(state="enabled")
            self.delete_button.config(state="disabled")  # Thường thì không nên cho xóa KH
        else:
            self.edit_button.config(state="disabled")
            self.delete_button.config(state="disabled")

    def deselect_tree(self, event):
        """Bỏ chọn tất cả các dòng khi nhấp ra ngoài."""
        if not self.tree.identify_region(event.x, event.y) == "heading":
            if not self.tree.focus():
                self.tree.selection_set()