import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# === IMPORT MỚI: TỪ MODEL ===
try:
    from models.driver_model import DriverModel
except ImportError as e:
    print(f"Lỗi Import trong driver_page: {e}")

# Định nghĩa màu sắc (cần dùng cho các con số)
COLOR_PRIMARY_TEAL = "#00A79E"


class DriverPage(ttk.Frame):
    """Trang Giao diện Quản lý Lái Xe (Kết nối Database)"""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.configure(padding=(20, 10))

        # === KHỞI TẠO MODEL ===
        try:
            self.db_model = DriverModel()
        except Exception as e:
            print(f"Không thể khởi tạo DriverModel: {e}")
            self.db_model = None

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
                                style="Primary.TButton",
                                command=self.open_add_driver_modal)
        add_button.pack(side="right", anchor="ne", pady=10)

        # --- 2. Hàng Thống Kê (SỬA ĐỔI) ---
        stat_frame = ttk.Frame(self, style="TFrame")
        stat_frame.pack(fill="x", expand=True, pady=10)

        # Card 1: Tổng Số Tài Xế
        card1 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(card1, text="Tổng Số Tài Xế", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        # SỬA: Gán self, bỏ màu
        self.total_label = ttk.Label(card1, text="Đang tải...", font=("Arial", 22, "bold"),
                                     style="light.TLabel")
        self.total_label.pack(anchor="w", pady=5)
        self.total_sublabel = ttk.Label(card1, text=" ", bootstyle="success")
        self.total_sublabel.pack(anchor="w")

        # Card 2: Tài Xế Hoạt Động
        card2 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card2.pack(side="left", fill="x", expand=True, padx=10)
        ttk.Label(card2, text="Tài Xế Hoạt Động", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        # SỬA: Gán self, bỏ màu
        self.active_label = ttk.Label(card2, text="Đang tải...", font=("Arial", 22, "bold"),
                                      style="light.TLabel")
        self.active_label.pack(anchor="w", pady=5)
        self.active_sublabel = ttk.Label(card2, text=" ", bootstyle="success")
        self.active_sublabel.pack(anchor="w")

        # Card 3: Tài Xế Không Hoạt Động
        card3 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card3.pack(side="left", fill="x", expand=True, padx=(10, 0))
        ttk.Label(card3, text="Tài Xế Không Hoạt Động", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        # SỬA: Gán self, bỏ màu
        self.inactive_label = ttk.Label(card3, text="Đang tải...", font=("Arial", 22, "bold"),
                                        style="light.TLabel")
        self.inactive_label.pack(anchor="w", pady=5)
        self.inactive_sublabel = ttk.Label(card3, text=" ", bootstyle="danger")
        self.inactive_sublabel.pack(anchor="w")

        # --- 3. Notebook (Tabs) ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="x", pady=10)

        tab_all = ttk.Frame(self.notebook)
        tab_active = ttk.Frame(self.notebook)
        tab_paused = ttk.Frame(self.notebook)
        tab_pending = ttk.Frame(self.notebook)

        self.notebook.add(tab_all, text="  Tất Cả  ")
        self.notebook.add(tab_active, text="  Đang Hoạt Động  ")
        self.notebook.add(tab_paused, text="  Tạm Ngưng  ")
        self.notebook.add(tab_pending, text="  Chờ Duyệt  ")

        # SỬA: Bind sự kiện để gọi hàm tìm kiếm/lọc
        self.notebook.bind("<<NotebookTabChanged>>", self.perform_filter_and_search)

        # --- 4. Thanh hành động (Sửa, Xóa, Tìm kiếm) ---
        action_bar = ttk.Frame(self, style="TFrame")
        action_bar.pack(fill="x", pady=5)

        self.edit_button = ttk.Button(action_bar, text="Sửa",
                                      bootstyle="outline-warning",
                                      state="disabled",
                                      command=self.open_edit_driver_modal)
        self.edit_button.pack(side="left", padx=(0, 5))

        self.delete_button = ttk.Button(action_bar, text="Xóa",
                                        bootstyle="outline-danger",
                                        state="disabled",
                                        command=self.delete_selected_driver)
        self.delete_button.pack(side="left", padx=5)

        # --- SỬA: Chức năng Tìm Kiếm ---
        self.search_placeholder = "Tìm mã tài xế, họ tên, SĐT..."
        self.search_entry = ttk.Entry(action_bar, width=50)
        self.search_entry.pack(side="right", fill="x", expand=True)
        self.search_entry.insert(0, self.search_placeholder)
        self.search_entry.config(foreground="gray")

        # Bind sự kiện cho ô tìm kiếm
        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)
        self.search_entry.bind("<KeyRelease>", self.perform_filter_and_search)
        # --- Kết thúc sửa ---

        # --- 5. Bảng Dữ Liệu (Treeview) ---
        table_container = ttk.Frame(self, style="TFrame")
        table_container.pack(fill="both", expand=True, pady=10)
        # (Giữ nguyên code định nghĩa cột, treeview, scrollbar...)
        columns = ("id", "name", "vehicle_category", "license", "email", "phone", "rating", "status")
        self.tree = ttk.Treeview(table_container, columns=columns, show='tree headings', height=15)
        self.tree.heading("#0", text=" ")
        self.tree.column("#0", width=50, anchor="center")
        self.tree.heading("id", text="Mã Tài Xế")
        self.tree.column("id", width=80)
        self.tree.heading("name", text="Họ Tên")
        self.tree.column("name", width=150)
        self.tree.heading("vehicle_category", text="Hạng Xe Lái")
        self.tree.column("vehicle_category", width=100, anchor="center")
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
        self.bind("<Button-1>", self.deselect_tree)
        action_bar.bind("<Button-1>", self.deselect_tree)
        # --- Kết thúc Treeview ---

        # --- 7. Phân trang (Pagination) ---
        pagination_frame = ttk.Frame(self, style="TFrame")
        pagination_frame.pack(fill="x", pady=(10, 0))
        self.pagination_label = ttk.Label(pagination_frame, text="Đang tải...", style="secondary.TLabel")
        self.pagination_label.pack(side="left")

        # --- 6. Tải dữ liệu lần đầu ---
        self.refresh_data()  # SỬA: Gọi hàm refresh_data()

    # === HÀM MỚI: Xử lý Placeholder cho ô tìm kiếm ===
    def on_search_focus_in(self, event):
        if self.search_entry.get() == self.search_placeholder:
            self.search_entry.delete(0, "end")
            self.search_entry.config(foreground="black")

    def on_search_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, self.search_placeholder)
            self.search_entry.config(foreground="gray")

    # === HÀM MỚI: Hàm tổng hợp tìm kiếm và lọc ===
    def perform_filter_and_search(self, event=None):
        search_term = self.search_entry.get()
        if search_term == self.search_placeholder:
            search_term = ""

        selected_tab_text = self.notebook.tab(self.notebook.select(), "text").strip()
        filter_status = None
        if selected_tab_text == "Đang Hoạt Động":
            filter_status = "Hoạt động"
        elif selected_tab_text == "Tạm Ngưng":
            filter_status = "Tạm ngưng"
        elif selected_tab_text == "Chờ Duyệt":
            filter_status = "Chờ duyệt"

        self.load_data_into_tree(filter_status=filter_status, search_term=search_term)

    # === HÀM MỚI: Tải số liệu thống kê ===
    def load_stats(self):
        if not self.db_model:
            return
        try:
            # 1. Gọi model (Giả định model có hàm get_driver_stats())
            stats = self.db_model.get_driver_stats()

            total = stats.get('total', 0)
            active = stats.get('active', 0)
            inactive = stats.get('inactive', 0)  # Tổng của Tạm ngưng và Chờ duyệt

            # 2. Cập nhật các Label chính
            self.total_label.config(text=f"{total:,.0f}")
            self.active_label.config(text=f"{active:,.0f}")
            self.inactive_label.config(text=f"{inactive:,.0f}")

            # 3. Cập nhật các Label phụ (tính %)
            inactive_percent = (inactive / total * 100) if total > 0 else 0

            self.total_sublabel.config(text="Tổng tài xế trong hệ thống")
            self.active_sublabel.config(text="Đang sẵn sàng nhận chuyến")
            self.inactive_sublabel.config(text=f"Chiếm {inactive_percent:.1f}% tổng số")

        except Exception as e:
            print(f"Lỗi khi tải số liệu tài xế: {e}")
            self.total_label.config(text="Lỗi")
            self.active_label.config(text="Lỗi")
            self.inactive_label.config(text="Lỗi")

    # === HÀM MỚI: Dùng để làm mới từ bên ngoài ===
    def refresh_data(self):
        """
        Hàm public mà file app.py chính sẽ gọi mỗi khi trang này được hiển thị.
        """
        print("Đang làm mới dữ liệu DriverPage...")
        self.load_stats()  # Tải các thẻ thống kê

        self.search_entry.delete(0, "end")
        self.on_search_focus_out(None)
        self.notebook.select(0)  # Chọn tab "Tất Cả"
        self.load_data_into_tree(filter_status=None, search_term="")  # Tải lại bảng
        self.tree.selection_set()  # Bỏ chọn

    def open_add_driver_modal(self):
        if self.db_model:
            # SỬA: Gọi refresh_data() sau khi thêm
            AddDriverModal(self, self.db_model, callback=self.refresh_data)
        else:
            print("Lỗi: Không thể mở form thêm tài xế vì Model chưa kết nối.")

    def delete_selected_driver(self):
        selected = self.tree.selection()
        if not selected: return

        item = self.tree.item(selected[0])
        driver_code = item['values'][0]

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa tài xế {driver_code}?"):
            success = self.db_model.delete_driver(driver_code)
            if success:
                messagebox.showinfo("Thành công", "Đã xóa tài xế.")
                self.refresh_data()  # SỬA: Gọi refresh_data()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa tài xế.")

    def open_edit_driver_modal(self):
        selected = self.tree.selection()
        if not selected: return

        item = self.tree.item(selected[0])
        driver_code = item['values'][0]

        # SỬA: Gọi refresh_data() sau khi sửa
        EditDriverModal(self, self.db_model, driver_code, callback=self.refresh_data)

    def on_tab_selected(self, event):
        """Được gọi khi người dùng nhấp vào một tab"""
        # SỬA: Hàm này giờ chỉ cần gọi hàm tổng
        self.perform_filter_and_search(event)

    # SỬA: load_data_into_tree giờ nhận cả search_term
    def load_data_into_tree(self, filter_status=None, search_term=None):
        """Xóa bảng và tải lại dữ liệu dựa trên trạng thái lọc và tìm kiếm"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.db_model:
            ttk.Label(self, text="Lỗi: Không thể kết nối Model.", bootstyle="danger").pack()
            return

        if search_term == self.search_placeholder:
            search_term = None

        try:
            # SỬA: Gọi hàm logic từ model với cả 2 tham số
            driver_data = self.db_model.get_all_drivers(status=filter_status, search=search_term)
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu tài xế: {e}")
            driver_data = []

        tag_map = {
            "Hoạt động": "hoatdong",
            "Tạm ngưng": "tamngung",
            "Chờ duyệt": "choduyet"
        }

        count = 0
        for item in driver_data:
            data_values = item
            status_value = item[-1]
            status_tag = tag_map.get(status_value, "")
            self.tree.insert("", "end", text="", values=data_values, tags=(status_tag,))
            count += 1

        # Cập nhật label phân trang
        self.pagination_label.config(text=f"Hiển thị {count} trong {count} kết quả.")

    def on_tree_select(self, event):
        """Kích hoạt nút Sửa/Xóa khi một dòng được chọn."""
        if self.tree.selection():
            self.edit_button.config(state="enabled")
            self.delete_button.config(state="enabled")
        else:
            self.edit_button.config(state="disabled")
            self.delete_button.config(state="disabled")  # Sửa: tắt cả nút xóa

    def deselect_tree(self, event):
        """Bỏ chọn tất cả các dòng khi nhấp ra ngoài."""
        if not self.tree.identify_region(event.x, event.y) == "heading":
            if not self.tree.focus():
                self.tree.selection_set()


# (Các lớp AddDriverModal và EditDriverModal giữ nguyên)
# (Vui lòng giữ nguyên code của 2 class này)
class AddDriverModal(tk.Toplevel):
    def __init__(self, parent, db_model, callback=None):
        tk.Toplevel.__init__(self, parent)
        self.title("Thêm Tài Xế Mới")
        self.db_model = db_model
        self.callback = callback
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        main_frame = ttk.Frame(self, padding=30, style='light')
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Thêm Tài Xế Mới", font=("Arial", 16, "bold"),
                  foreground=COLOR_PRIMARY_TEAL).pack(pady=(0, 10))
        ttk.Label(main_frame, text="Nhập thông tin tài xế mới vào mẫu bên dưới.",
                  bootstyle="secondary").pack(pady=(0, 20))

        self.create_form_widgets(main_frame)

        button_frame = ttk.Frame(main_frame, style='light')
        button_frame.pack(fill="x", pady=20)

        ttk.Button(button_frame, text="Lưu", command=self.save_driver, bootstyle="success").pack(side="right")
        ttk.Button(button_frame, text="Hủy", command=self.destroy, bootstyle="secondary-outline").pack(side="right",
                                                                                                       padx=10)

    def create_form_widgets(self, parent):
        form_frame = ttk.Frame(parent, style='light')
        form_frame.pack(fill="x")

        form_frame.columnconfigure(1, weight=1)

        # === THÊM 4 DÒNG NÀY ===
        ttk.Label(form_frame, text="Mã Tài Xế", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                 sticky="w",
                                                                                 pady=(10, 0))
        self.driver_code_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.driver_code_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 10), ipady=5)
        # ==========================

        # 1. Họ Tên (Sửa row=0 thành row=2, row=1 thành row=3)
        ttk.Label(form_frame, text="Họ Tên", font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=2, sticky="w",
                                                                              pady=(10, 0))
        self.name_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.name_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=(0, 10), ipady=5)

        # 2. Email (Sửa row=2 thành row=4, row=3 thành row=5)
        ttk.Label(form_frame, text="Email", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=(10, 0))
        self.email_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.email_entry.grid(row=5, column=0, sticky="ew", padx=(0, 10), ipady=5)

        # (Sửa tất cả các 'row' tiếp theo, tăng lên 2 đơn vị)
        # 3. Số Điện Thoại (row=4, row=5)
        ttk.Label(form_frame, text="Số Điện Thoại", font=("Arial", 10, "bold")).grid(row=4, column=1, sticky="w",
                                                                                     pady=(10, 0))
        self.phone_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.phone_entry.grid(row=5, column=1, sticky="ew", padx=(10, 0), ipady=5)

        # 4. Hạng Xe Lái (row=6, row=7)
        ttk.Label(form_frame, text="Hạng Xe Lái", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky="w",
                                                                                   pady=(10, 0))
        self.vehicle_combo = ttk.Combobox(form_frame, values=["Xe 4 Chỗ", "Xe 7 Chỗ", "Xe Bán Tải"], state="readonly")
        self.vehicle_combo.set("Xe 4 Chỗ")
        self.vehicle_combo.grid(row=7, column=0, sticky="ew", padx=(0, 10), ipady=5)

        # 5. Số Bằng Lái (row=6, row=7)
        ttk.Label(form_frame, text="Số Bằng Lái", font=("Arial", 10, "bold")).grid(row=6, column=1, sticky="w",
                                                                                   pady=(10, 0))
        self.license_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.license_entry.grid(row=7, column=1, sticky="ew", padx=(10, 0), ipady=5)

        # 6. Trạng Thái (row=8, row=9)
        ttk.Label(form_frame, text="Trạng Thái", font=("Arial", 10, "bold")).grid(row=8, column=0, columnspan=2,
                                                                                  sticky="w", pady=(10, 0))
        self.status_combo = ttk.Combobox(form_frame, values=["Hoạt động", "Tạm ngưng", "Chờ duyệt"], state="readonly")
        self.status_combo.set("Chờ duyệt")
        self.status_combo.grid(row=9, column=0, columnspan=2, sticky="ew", padx=(0, 10), ipady=5)

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

    def save_driver(self):
        # 1. Lấy dữ liệu
        data = {
            'driver_code': self.driver_code_entry.get(),  # <-- THÊM DÒNG NÀY
            'name': self.name_entry.get(),
            'email': self.email_entry.get(),
            'phone': self.phone_entry.get(),
            'vehicle_category': self.vehicle_combo.get(),
            'license': self.license_entry.get(),
            'status': self.status_combo.get()
        }

        # Sửa: Kiểm tra driver_code và name/phone
        if not data['driver_code'] or not data['name'] or not data['phone']:
            messagebox.showerror("Lỗi", "Vui lòng nhập Mã Tài Xế, Họ Tên và SĐT.")
            return
        # 2. Gọi hàm thêm trong Model
        success = self.db_model.add_driver(data)

        if success:
            messagebox.showinfo("Thành công", "Đã thêm tài xế mới.")
            self.destroy()
            if self.callback:
                self.callback()  # Gọi lại hàm load dữ liệu sau khi thêm
        else:
            messagebox.showerror("Lỗi", "Không thể lưu tài xế vào CSDL. Vui lòng kiểm tra lại kết nối và dữ liệu.")


class EditDriverModal(tk.Toplevel):
    def __init__(self, parent, db_model, driver_code, callback=None):
        super().__init__(parent)
        self.db_model = db_model
        self.driver_code = driver_code
        self.callback = callback
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        main_frame = ttk.Frame(self, padding=30, style='light')
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Sửa Thông Tin Tài Xế", font=("Arial", 16, "bold"),
                  foreground="#00A79E").pack(pady=(0, 10))

        # Lấy dữ liệu tài xế
        # SỬA: Tối ưu hơn là tạo hàm get_driver_by_id(code) trong model
        all_data = self.db_model.get_all_drivers()
        driver_data = next((d for d in all_data if d[0] == driver_code), None)

        self.create_form_widgets(main_frame, driver_data)

        button_frame = ttk.Frame(main_frame, style='light')
        button_frame.pack(fill="x", pady=20)

        ttk.Button(button_frame, text="Lưu", command=self.save_driver, bootstyle="success").pack(side="right")
        ttk.Button(button_frame, text="Hủy", command=self.destroy, bootstyle="secondary-outline").pack(side="right",
                                                                                                       padx=10)

    def create_form_widgets(self, parent, driver_data):
        form_frame = ttk.Frame(parent, style='light')
        form_frame.pack(fill="x")

        form_frame.columnconfigure(1, weight=1)

        # --- Họ Tên ---
        ttk.Label(form_frame, text="Họ Tên", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2,
                                                                              sticky="w", pady=(10, 0))
        self.name_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 10), ipady=5)
        self.name_entry.insert(0, driver_data[1] if driver_data else "")

        # --- Email ---
        ttk.Label(form_frame, text="Email", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w",
                                                                             pady=(10, 0))
        self.email_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.email_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10), ipady=5)
        self.email_entry.insert(0, driver_data[4] if driver_data else "")

        # --- Số Điện Thoại ---
        ttk.Label(form_frame, text="Số Điện Thoại", font=("Arial", 10, "bold")).grid(row=2, column=1, sticky="w",
                                                                                     pady=(10, 0))
        self.phone_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.phone_entry.grid(row=3, column=1, sticky="ew", padx=(10, 0), ipady=5)
        self.phone_entry.insert(0, driver_data[5] if driver_data else "")

        # --- Hạng Xe Lái ---
        ttk.Label(form_frame, text="Hạng Xe Lái", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w",
                                                                                   pady=(10, 0))
        self.vehicle_combo = ttk.Combobox(form_frame, values=["Xe 4 Chỗ", "Xe 7 Chỗ", "Xe Bán Tải"],
                                          state="readonly")
        self.vehicle_combo.grid(row=5, column=0, sticky="ew", padx=(0, 10), ipady=5)
        self.vehicle_combo.set(driver_data[2] if driver_data else "Xe 4 Chỗ")

        # --- Số Bằng Lái ---
        ttk.Label(form_frame, text="Số Bằng Lái", font=("Arial", 10, "bold")).grid(row=4, column=1, sticky="w",
                                                                                   pady=(10, 0))
        self.license_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.license_entry.grid(row=5, column=1, sticky="ew", padx=(10, 0), ipady=5)
        self.license_entry.insert(0, driver_data[3] if driver_data else "")

        # --- Trạng Thái ---
        ttk.Label(form_frame, text="Trạng Thái", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=2,
                                                                                  sticky="w", pady=(10, 0))
        self.status_combo = ttk.Combobox(form_frame, values=["Hoạt động", "Tạm ngưng", "Chờ duyệt"],
                                         state="readonly")
        self.status_combo.grid(row=7, column=0, columnspan=2, sticky="ew", padx=(0, 10), ipady=5)
        self.status_combo.set(driver_data[7] if driver_data else "Chờ duyệt")

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

    def save_driver(self):
        data = {
            'name': self.name_entry.get(),
            'email': self.email_entry.get(),
            'phone': self.phone_entry.get(),
            'vehicle_category': self.vehicle_combo.get(),
            'license': self.license_entry.get(),
            'status': self.status_combo.get()
        }

        if not all(data.values()):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        success = self.db_model.update_driver(self.driver_code, data)
        if success:
            messagebox.showinfo("Thành công", "Đã cập nhật tài xế.")
            self.destroy()
            if self.callback:
                self.callback()
        else:
            messagebox.showerror("Lỗi", "Không thể cập nhật tài xế.")