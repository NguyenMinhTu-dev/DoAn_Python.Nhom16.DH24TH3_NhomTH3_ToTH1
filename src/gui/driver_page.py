import tkinter as tk
from tkinter import font as tkfont
from  tkinter import messagebox
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

        # --- XÓA DỮ LIỆU MẪU (master_driver_data) ---
        # (self.master_driver_data đã bị xóa)

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
                                bootstyle="success",
                                command= self.open_add_driver_modal)
        add_button.pack(side="right", anchor="ne", pady=10)


        # --- 2. Hàng Thống Kê ---
        stat_frame = ttk.Frame(self, style="TFrame")
        stat_frame.pack(fill="x", expand=True, pady=10)

        # (Thẻ thống kê - Tạm thời giữ số liệu mẫu, bạn có thể thay bằng hàm gọi model)
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
        notebook = ttk.Notebook(self)
        notebook.pack(fill="x", pady=10)

        tab_all = ttk.Frame(notebook)
        tab_active = ttk.Frame(notebook)
        tab_paused = ttk.Frame(notebook)
        tab_pending = ttk.Frame(notebook)

        notebook.add(tab_all, text="  Tất Cả  ")
        notebook.add(tab_active, text="  Đang Hoạt Động  ")
        notebook.add(tab_paused, text="  Tạm Ngưng  ")
        notebook.add(tab_pending, text="  Chờ Duyệt  ")

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        # --- 4. Thanh hành động (Sửa, Xóa, Tìm kiếm) ---
        action_bar = ttk.Frame(self, style="TFrame")
        action_bar.pack(fill="x", pady=5)

        self.edit_button = ttk.Button(action_bar, text="Sửa",
                                      bootstyle="outline-warning",
                                      state="disabled",
                                      command= self.open_edit_driver_modal)
        self.edit_button.pack(side="left", padx=(0, 5))

        self.delete_button = ttk.Button(action_bar, text="Xóa",
                                        bootstyle="outline-danger",
                                        state="disabled",
                                        command= self.delete_selected_driver)
        self.delete_button.pack(side="left", padx=5)

        search_entry = ttk.Entry(action_bar, width=50)
        search_entry.pack(side="right", fill="x", expand=True)
        search_entry.insert(0, "Tìm mã tài xế, họ tên, SĐT...")

        # --- 5. Bảng Dữ Liệu (Treeview) ---
        table_container = ttk.Frame(self, style="TFrame")
        table_container.pack(fill="both", expand=True, pady=10)

        # Sửa: Tên cột phải khớp với CSDL
        columns = ("id", "name", "vehicle_category", "license", "email", "phone", "rating", "status")

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
        self.tree.heading("vehicle_category", text="Hạng Xe Lái")  # Sửa
        self.tree.column("vehicle_category", width=100, anchor="center")  # Sửa
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
    def open_add_driver_modal(self):
                if self.db_model:
                    AddDriverModal(self, self.db_model, callback=lambda: self.load_data_into_tree())
                else:
                    print("Lỗi: Không thể mở form thêm tài xế vì Model chưa kết nối.")

    def delete_selected_driver(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        driver_code = item['values'][0]

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa tài xế {driver_code}?"):
            success = self.db_model.delete_driver(driver_code)
            if success:
                messagebox.showinfo("Thành công", "Đã xóa tài xế.")
                self.load_data_into_tree()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa tài xế.")

    def open_edit_driver_modal(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item['values']
        driver_code = values[0]  # ma_tai_xe

        # Tạo form tương tự AddDriverModal nhưng có dữ liệu sẵn
        EditDriverModal(self, self.db_model, driver_code, callback=lambda: self.load_data_into_tree())

    def on_tab_selected(self, event):
        """Được gọi khi người dùng nhấp vào một tab"""
        selected_tab_text = event.widget.tab(event.widget.select(), "text").strip()

        # Bỏ chọn bất kỳ dòng nào đang chọn
        self.tree.selection_set()

        # Truyền giá trị Tiếng Việt của CSDL
        if selected_tab_text == "Tất Cả":
            self.load_data_into_tree(filter_status=None)
        elif selected_tab_text == "Đang Hoạt Động":
            self.load_data_into_tree(filter_status="Hoạt động")
        elif selected_tab_text == "Tạm Ngưng":
            self.load_data_into_tree(filter_status="Tạm ngưng")
        elif selected_tab_text == "Chờ Duyệt":
            self.load_data_into_tree(filter_status="Chờ duyệt")

    def load_data_into_tree(self, filter_status=None):
        """Xóa bảng và tải lại dữ liệu dựa trên trạng thái lọc"""

        # Xóa tất cả dữ liệu cũ trong bảng
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.db_model:
            ttk.Label(self, text="Lỗi: Không thể kết nối Model.", bootstyle="danger").pack()
            return

        # === LẤY DỮ LIỆU TỪ DATABASE ===
        try:
            # Gọi hàm logic từ model
            driver_data = self.db_model.get_all_drivers(status=filter_status)
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu tài xế: {e}")
            driver_data = []

        # Tạo map (ánh xạ) từ giá trị trạng thái sang tag
        tag_map = {
            "Hoạt động": "hoatdong",
            "Tạm ngưng": "tamngung",
            "Chờ duyệt": "choduyet"
        }

        # Lặp qua DỮ LIỆU TỪ DB và thêm vào bảng
        count = 0
        for item in driver_data:
            # item là một tuple, vd: ('TX001', 'Nguyễn Văn An', 'Xe 4 Chỗ', ...)

            # Đảm bảo thứ tự cột khớp:
            # (id, name, vehicle_category, license, email, phone, rating, status)
            data_values = item

            # Lấy giá trị trạng thái (cột cuối cùng)
            status_value = item[-1]
            # Lấy tag màu tương ứng
            status_tag = tag_map.get(status_value, "")

            self.tree.insert("", "end", text="", values=data_values, tags=(status_tag,))
            count += 1

        # Dòng này bây giờ sẽ chạy được
#        self.pagination_label.config(text=f"Hiển thị {count} trong {count} kết quả.")

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

        # 1. Họ Tên
        ttk.Label(form_frame, text="Họ Tên", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w",
                                                                              pady=(10, 0))
        self.name_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 10), ipady=5)

        # 2. Email (Left)
        ttk.Label(form_frame, text="Email", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.email_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.email_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10), ipady=5)

        # 3. Số Điện Thoại (Right)
        ttk.Label(form_frame, text="Số Điện Thoại", font=("Arial", 10, "bold")).grid(row=2, column=1, sticky="w",
                                                                                     pady=(10, 0))
        self.phone_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.phone_entry.grid(row=3, column=1, sticky="ew", padx=(10, 0), ipady=5)

        # 4. Hạng Xe Lái (Left - Combobox)
        ttk.Label(form_frame, text="Hạng Xe Lái", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w",
                                                                                   pady=(10, 0))
        self.vehicle_combo = ttk.Combobox(form_frame, values=["Xe 4 Chỗ", "Xe 7 Chỗ", "Xe Bán Tải"], state="readonly")
        self.vehicle_combo.set("Xe 4 Chỗ")
        self.vehicle_combo.grid(row=5, column=0, sticky="ew", padx=(0, 10), ipady=5)

        # 5. Số Bằng Lái (Right)
        ttk.Label(form_frame, text="Số Bằng Lái", font=("Arial", 10, "bold")).grid(row=4, column=1, sticky="w",
                                                                                   pady=(10, 0))
        self.license_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.license_entry.grid(row=5, column=1, sticky="ew", padx=(10, 0), ipady=5)

        # 6. Trạng Thái (Full width)
        ttk.Label(form_frame, text="Trạng Thái", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=2,
                                                                                  sticky="w", pady=(10, 0))
        self.status_combo = ttk.Combobox(form_frame, values=["Hoạt động", "Tạm ngưng", "Chờ duyệt"], state="readonly")
        self.status_combo.set("Chờ duyệt")
        self.status_combo.grid(row=7, column=0, columnspan=2, sticky="ew", padx=(0, 10), ipady=5)

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)


    def save_driver(self):
        # 1. Lấy dữ liệu
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
        data = self.db_model.get_all_drivers()  # hoặc tạo hàm get_driver_by_id
        driver_data = next((d for d in data if d[0] == driver_code), None)

        self.create_form_widgets(main_frame, driver_data)

        button_frame = ttk.Frame(main_frame, style='light')
        button_frame.pack(fill="x", pady=20)

        ttk.Button(button_frame, text="Lưu", command=self.save_driver, bootstyle="success").pack(side="right")
        ttk.Button(button_frame, text="Hủy", command=self.destroy, bootstyle="secondary-outline").pack(side="right", padx=10)

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
