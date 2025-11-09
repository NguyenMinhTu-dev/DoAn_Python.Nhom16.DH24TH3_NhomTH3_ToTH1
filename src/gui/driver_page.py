# driver_page.py
import tkinter as tk
from tkinter import font as tkfont
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# Định nghĩa màu sắc (cần dùng cho các con số)
COLOR_PRIMARY_TEAL = "#00A79E"


class DriverPage(ttk.Frame):
    """Trang Giao diện Quản lý Lái Xe (với Tabs Filter)"""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.configure(padding=(20, 10))

        # --- LƯU TRỮ DỮ LIỆU GỐC ---
        # Chúng ta lưu dữ liệu gốc ở đây để có thể lọc
        self.master_driver_data = [
            ("TX001", "Nguyễn Văn An", "Xe 4 Chỗ", "123456789", "nguyenvana@example.com", "0901234567", "4.8 Sao",
             "Hoạt động", "hoatdong"),
            ("TX002", "Trần Văn Bình", "Xe 7 Chỗ", "234567890", "tranvanbinh@example.com", "0912345678", "4.5 Sao",
             "Hoạt động", "hoatdong"),
            ("TX003", "Lê Thị Cẩm", "Xe 4 Chỗ", "345678901", "lethicam@example.com", "0923456789", "4.2 Sao",
             "Tạm ngưng", "tamngung"),
            ("TX004", "Phạm Văn Dũng", "Xe 4 Chỗ", "456789012", "phamvandung@example.com", "0934567890", "4.9 Sao",
             "Hoạt động", "hoatdong"),
            ("TX005", "Hoàng Thị Em", "Xe 4 Chỗ", "567890123", "hoangthiem@example.com", "0945678901", "N/A",
             "Chờ duyệt", "choduyet")
        ]

        # --- 1. Tiêu đề & Nút Thêm Mới ---
        title_frame = ttk.Frame(self, style="TFrame")
        title_frame.pack(fill="x", anchor="n", pady=(0, 10))

        left_title_frame = ttk.Frame(title_frame, style="TFrame")
        left_title_frame.pack(side="left", fill="x", expand=True)

        ttk.Label(left_title_frame, text="Quản Lý Tài Xế",
                  font=("Arial", 24, "bold"),
                  style="TLabel").pack(anchor="w")
        ttk.Label(left_title_frame, text="Xem và quản lý thông tin tài xế trong hệ thống.",
                  style="secondary.TLabel").pack(anchor="w")

        add_button = ttk.Button(title_frame, text="Thêm Tài Xế",
                                bootstyle="success")
        add_button.pack(side="right", anchor="ne", pady=10)

        # --- 2. Hàng Thống Kê ---
        stat_frame = ttk.Frame(self, style="TFrame")
        stat_frame.pack(fill="x", expand=True, pady=10)
        # (Code của 3 thẻ Card thống kê...)
        card1 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(card1, text="Tổng Số Tài Xế", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card1, text="573", font=("Arial", 22, "bold"),
                  style="light.TLabel", foreground=COLOR_PRIMARY_TEAL).pack(anchor="w", pady=5)
        ttk.Label(card1, text="+24 tài xế mới trong tháng", bootstyle="success").pack(anchor="w")
        card2 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card2.pack(side="left", fill="x", expand=True, padx=10)
        ttk.Label(card2, text="Tài Xế Hoạt Động", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card2, text="498", font=("Arial", 22, "bold"),
                  style="light.TLabel", foreground=COLOR_PRIMARY_TEAL).pack(anchor="w", pady=5)
        ttk.Label(card2, text="+5% so với tuần trước", bootstyle="success").pack(anchor="w")
        card3 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card3.pack(side="left", fill="x", expand=True, padx=(10, 0))
        ttk.Label(card3, text="Tài Xế Không Hoạt Động", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        ttk.Label(card3, text="75", font=("Arial", 22, "bold"),
                  style="light.TLabel", foreground=COLOR_PRIMARY_TEAL).pack(anchor="w", pady=5)
        ttk.Label(card3, text="13.0% tổng số tài xế", bootstyle="danger").pack(anchor="w")

        # --- 3. Notebook (Tabs) ---
        # Tabs này bây giờ KHÔNG chứa bảng, chỉ là các Frame trống để chọn
        notebook = ttk.Notebook(self)
        notebook.pack(fill="x", pady=10)  # Bỏ expand=True

        tab_all = ttk.Frame(notebook)
        tab_active = ttk.Frame(notebook)
        tab_paused = ttk.Frame(notebook)
        tab_pending = ttk.Frame(notebook)

        notebook.add(tab_all, text="  Tất Cả  ")
        notebook.add(tab_active, text="  Đang Hoạt Động  ")
        notebook.add(tab_paused, text="  Tạm Ngưng  ")
        notebook.add(tab_pending, text="  Chờ Duyệt  ")

        # === GÁN SỰ KIỆN KHI CHỌN TAB ===
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        # --- 4. Thanh hành động (Sửa, Xóa, Tìm kiếm) ---
        # Đã dời ra ngoài, nằm dưới Tabs
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
        search_entry.insert(0, "Tìm mã tài xế, họ tên, SĐT...")

        # --- 5. Bảng Dữ Liệu (Treeview) ---
        # Đã dời ra ngoài, nằm dưới Thanh hành động
        table_container = ttk.Frame(self, style="TFrame")
        table_container.pack(fill="both", expand=True, pady=10)

        columns = ("id", "name", "vehicle", "license", "email", "phone", "rating", "status")

        self.tree = ttk.Treeview(table_container,
                                 columns=columns,
                                 show='tree headings',
                                 height=15)

        self.tree.heading("#0", text=" ")
        self.tree.column("#0", width=50, anchor="center")

        self.tree.heading("id", text="Mã Tài Xế")
        self.tree.column("id", width=80)
        self.tree.heading("name", text="Họ Tên")
        self.tree.column("name", width=150)
        # (Các cột khác)
        self.tree.heading("vehicle", text="Loại Xe")
        self.tree.column("vehicle", width=80, anchor="center")
        self.tree.heading("license", text="Số Bằng Lái")
        self.tree.column("license", width=100, anchor="center")
        self.tree.heading("email", text="Email")
        self.tree.column("email", width=180)
        self.tree.heading("phone", text="Số Điện Thoại")
        self.tree.column("phone", width=120)
        self.tree.heading("rating", text="Đánh Giá")
        self.tree.column("rating", width=80, anchor="center")
        self.tree.heading("status", text="Trạng Thái")
        self.tree.column("status", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure('hoatdong', foreground='#28a745')
        self.tree.tag_configure('tamngung', foreground='#fd7e14')
        self.tree.tag_configure('choduyet', foreground='#17a2b8')

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        # Cần bind cho cả các thành phần khác để bỏ chọn
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

        # Bỏ chọn bất kỳ dòng nào đang chọn
        self.tree.selection_set()

        if selected_tab_text == "Tất Cả":
            self.load_data_into_tree(filter_status=None)
        elif selected_tab_text == "Đang Hoạt Động":
            self.load_data_into_tree(filter_status="Hoạt động")
        elif selected_tab_text == "Tạm Ngưng":
            self.load_data_into_tree(filter_status="Tạm ngưng")
        elif selected_tab_text == "Chờ Duyệt":
            self.load_data_into_tree(filter_status="Chờ duyệt")

    # --- HÀM MỚI: TẢI DỮ LIỆU CÓ LỌC ---
    def load_data_into_tree(self, filter_status=None):
        """Xóa bảng và tải lại dữ liệu dựa trên trạng thái lọc"""

        # Xóa tất cả dữ liệu cũ trong bảng
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lặp qua DỮ LIỆU GỐC và thêm vào bảng nếu khớp
        for item in self.master_driver_data:
            status_tag = item[-1]  # Tag màu (vd: 'hoatdong')
            data_values = item[:-1]  # Dữ liệu (bỏ tag)
            status_value = data_values[7]  # Giá trị trạng thái (vd: "Hoạt động")

            # Nếu filter_status=None (Tất cả) HOẶC trạng thái khớp
            if filter_status is None or status_value == filter_status:
                self.tree.insert("", "end", text="", values=data_values, tags=(status_tag,))

    def on_tree_select(self, event):
        """Kích hoạt nút Sửa/Xóa khi một dòng được chọn."""
        if self.tree.selection():
            self.edit_button.config(state="enabled")
            self.delete_button.config(state="enabled")
        else:
            self.edit_button.config(state="disabled")
            self.delete_button.config(state="disabled")

    def deselect_tree(self, event):
        """Bỏ chọn tất cả các dòng khi nhấp ra ngoài."""
        if not self.tree.identify_region(event.x, event.y) == "heading":
            if not self.tree.focus():
                self.tree.selection_set()