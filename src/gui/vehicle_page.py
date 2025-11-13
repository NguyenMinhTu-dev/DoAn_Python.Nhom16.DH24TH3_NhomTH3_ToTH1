import tkinter as tk
from tkinter import font as tkfont
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from tkinter import messagebox
import datetime
from ttkbootstrap.widgets import DateEntry


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
                                bootstyle="success",
                                command = self.open_add_vehicle_modal)

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
                                      state="disabled",
                                      command= self.open_edit_vehicle_modal)
        self.edit_button.pack(side="left", padx=(0, 5))

        self.delete_button = ttk.Button(action_bar, text="Xóa",
                                        bootstyle="outline-danger",
                                        state="disabled",
                                        command= self.delete_selected_vehicle)
        self.delete_button.pack(side="left", padx=5)

        search_entry = ttk.Entry(action_bar, width=50)
        search_entry.pack(side="right", fill="x", expand=True)
        search_entry.insert(0, "Tìm theo biển số xe, loại xe...")

        # --- 5. Bảng Dữ Liệu (Treeview) ---
        table_container = ttk.Frame(self, style="TFrame")
        table_container.pack(fill="both", expand=True, pady=10)

        # Các cột này PHẢI KHỚP với câu query SELECT
        columns = ("id_vehicle","plate", "type","mileage", "last_maintenance", "status","driver_name")

        self.tree = ttk.Treeview(table_container,
                                 columns=columns,
                                 show='tree headings',
                                 height=15)

        self.tree.heading("#0", text=" ")
        self.tree.column("#0", width=50, anchor="center")
        self.tree.heading("id_vehicle", text="Mã Xe")
        self.tree.column("id_vehicle", width=50, anchor="center")
        self.tree.heading("plate", text="Biển Số Xe")
        self.tree.column("plate", width=120, anchor="center")
        self.tree.heading("type", text="Loại Xe")
        self.tree.column("type", width=150)

        self.tree.heading("mileage", text="Số Km")
        self.tree.column("mileage", width=100, anchor="e")
        self.tree.heading("last_maintenance", text="Bảo Trì Lần Cuối")
        self.tree.column("last_maintenance", width=150, anchor="center")
        self.tree.heading("status", text="Trạng Thái")
        self.tree.column("status", width=120, anchor="center")
        self.tree.heading("driver_name", text="Mã Tài Xế Phụ Trách")
        self.tree.column("driver_name", width=120)

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
    def open_add_vehicle_modal(self):
            if self.db_model:
                AddVehicleModal(self, self.db_model, callback=lambda: self.load_data_into_tree())
            else:
                messagebox.showerror("Lỗi", "Không thể mở form thêm xe vì Model chưa kết nối.")

    def open_edit_vehicle_modal(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        vehicle_id = item['values'][0]  # id_phuong_tien

        vehicle_data = self.db_model.get_vehicle_by_id(vehicle_id)
        if not vehicle_data:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu phương tiện.")
            return

        EditVehicleModal(self, self.db_model, vehicle_data, callback=lambda: self.load_data_into_tree())

    def delete_selected_vehicle(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        plate = item['values'][1]

        if not plate:  # Kiểm tra None/empty
            messagebox.showerror("Lỗi", "Biển số xe không hợp lệ.")
            return

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa phương tiện {plate}?"):
            success = self.db_model.delete_vehicle(plate)
            if success:
                messagebox.showinfo("Thành công", f"Đã xóa phương tiện {plate}.")
                self.load_data_into_tree()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa phương tiện.")

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
    # === FORM THÊM/SỬA XE ===
class AddVehicleModal(tk.Toplevel):
    """
    Modal để thêm xe mới.
    parent: VehiclePage để reload treeview
    db_model: instance của VehicleModel
    callback: hàm gọi lại khi thêm thành công (ví dụ reload treeview)
    """

    def __init__(self, parent, db_model, callback=None):
        super().__init__(parent)
        self.parent = parent
        self.db_model = db_model
        self.callback = callback

        self.title("Thêm Xe Mới")
        self.geometry("520x500")
        self.resizable(False, False)

        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="🛞 Thêm Xe Mới", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 15)
        )

        # Biển số
        ttk.Label(container, text="Biển số xe:").grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.plate_entry = ttk.Entry(container, width=22)
        self.plate_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=2)

        # Loại xe
        ttk.Label(container, text="Loại xe:").grid(row=1, column=1, sticky="w")
        self.type_entry = ttk.Entry(container, width=22)
        self.type_entry.grid(row=2, column=1, sticky="ew", pady=2)

        # Số km
        ttk.Label(container, text="Số km:").grid(row=3, column=0, sticky="w", pady=(10, 0))
        self.mileage_entry = ttk.Entry(container, width=22)
        self.mileage_entry.grid(row=4, column=0, sticky="ew", padx=(0, 10), pady=2)

        # Bảo trì lần cuối
        ttk.Label(container, text="Bảo trì lần cuối:").grid(row=3, column=1, sticky="w", pady=(10, 0))
        self.maintenance_entry = DateEntry(container, dateformat="%d/%m/%Y", bootstyle="info", width=22)
        self.maintenance_entry.grid(row=4, column=1, sticky="ew", pady=2)
        self.maintenance_entry.set_date(datetime.date.today())

        # Tài xế phụ trách (Combobox)
        ttk.Label(container, text="Tài xế phụ trách:").grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.driver_combo = ttk.Combobox(container, width=50, state="readonly")
        self.driver_combo.grid(row=6, column=0, columnspan=2, sticky="ew", pady=2)

        # Load danh sách tài xế
        self.load_driver_names()

        # Trạng thái
        ttk.Label(container, text="Trạng thái:").grid(row=7, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.status_combo = ttk.Combobox(container, values=["Hoạt động", "Bảo trì", "Ngừng hoạt động"], state="readonly")
        self.status_combo.grid(row=8, column=0, columnspan=2, sticky="ew", pady=2)
        self.status_combo.current(0)

        # Nút Lưu / Hủy
        button_frame = ttk.Frame(container)
        button_frame.grid(row=9, column=0, columnspan=2, pady=25, sticky="ew")
        ttk.Button(button_frame, text="💾 Lưu", bootstyle="success", command=self.save_vehicle).pack(
            side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(button_frame, text="❌ Hủy", bootstyle="secondary", command=self.destroy).pack(
            side="left", expand=True, fill="x", padx=(5, 0))

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

    def load_driver_names(self):
        """Load danh sách tài xế từ db_model để cho combobox chọn"""
        try:
            drivers = self.db_model.get_all_drivers(status="Hoạt động")
            names = [driver[1] for driver in drivers]  # cột 1 là tên
            self.driver_combo['values'] = names
            if names:
                self.driver_combo.current(0)

            # Mapping: tên -> mã
            self.driver_map = {driver[1]: driver[0] for driver in drivers}

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách tài xế: {e}")
            self.driver_map = {}

    def save_vehicle(self):
        try:
            plate = self.plate_entry.get().strip()
            if not plate:
                messagebox.showerror("Lỗi", "Vui lòng nhập biển số xe.")
                return

            driver_name = self.driver_combo.get().strip()
            driver_code = self.driver_map.get(driver_name, None)

            data = {
                'plate': plate,
                'type': self.type_entry.get(),
                'mileage': int(self.mileage_entry.get()),
                'last_maintenance': self.maintenance_entry.get_date().strftime("%Y-%m-%d"),
                'status': self.status_combo.get(),
                'driver_code': driver_code
            }

            success = self.db_model.add_vehicle(data)
            if success:
                messagebox.showinfo("Thành công", "Xe mới đã được thêm.")
                self.destroy()
                if self.callback:
                    self.callback()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm xe: {e}")
class EditVehicleModal(tk.Toplevel):
    """
    Modal chỉnh sửa thông tin phương tiện.
    parent: VehiclePage để reload treeview
    db_model: instance của VehicleModel
    vehicle_data: dictionary dữ liệu phương tiện
    callback: hàm gọi lại khi cập nhật thành công
    """
    def __init__(self, parent, db_model, vehicle_data, callback=None):
        super().__init__(parent)
        self.parent = parent
        self.db_model = db_model
        self.vehicle_data = vehicle_data
        self.callback = callback

        self.title("Sửa Phương Tiện")
        self.geometry("520x500")
        self.resizable(False, False)

        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="🛞 Sửa Phương Tiện", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 15)
        )

        # Biển số xe (có thể cho sửa)
        ttk.Label(container, text="Biển số xe:").grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.plate_entry = ttk.Entry(container, width=22)
        self.plate_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=2)
        self.plate_entry.insert(0, vehicle_data['bien_so_xe'])

        # Loại xe
        ttk.Label(container, text="Loại xe:").grid(row=1, column=1, sticky="w")
        self.type_entry = ttk.Entry(container, width=22)
        self.type_entry.grid(row=2, column=1, sticky="ew", pady=2)
        self.type_entry.insert(0, vehicle_data['loai_xe'])

        # Số km
        ttk.Label(container, text="Số km:").grid(row=3, column=0, sticky="w", pady=(10, 0))
        self.mileage_entry = ttk.Entry(container, width=22)
        self.mileage_entry.grid(row=4, column=0, sticky="ew", padx=(0, 10), pady=2)
        self.mileage_entry.insert(0, vehicle_data['so_km_da_di'])

        # Bảo trì lần cuối
        ttk.Label(container, text="Bảo trì lần cuối:").grid(row=3, column=1, sticky="w", pady=(10, 0))
        self.maintenance_entry = DateEntry(container, dateformat="%d/%m/%Y", bootstyle="info", width=22)
        self.maintenance_entry.grid(row=4, column=1, sticky="ew", pady=2)
        if vehicle_data['ngay_bao_tri_cuoi']:
            self.maintenance_entry.set_date(vehicle_data['ngay_bao_tri_cuoi'])
        else:
            self.maintenance_entry.set_date(datetime.date.today())

        # Tài xế phụ trách
        ttk.Label(container, text="Tài xế phụ trách:").grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.driver_combo = ttk.Combobox(container, width=50, state="readonly")
        self.driver_combo.grid(row=6, column=0, columnspan=2, sticky="ew", pady=2)
        self.load_driver_names()
        # Chọn tài xế hiện tại
        current_driver = vehicle_data.get('ma_tai_xe_phu_trach')
        if current_driver and current_driver in self.driver_map.values():
            name = [k for k, v in self.driver_map.items() if v == current_driver][0]
            self.driver_combo.set(name)

        # Trạng thái
        ttk.Label(container, text="Trạng thái:").grid(row=7, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.status_combo = ttk.Combobox(container, values=["Hoạt động", "Bảo trì", "Ngừng hoạt động"], state="readonly")
        self.status_combo.grid(row=8, column=0, columnspan=2, sticky="ew", pady=2)
        self.status_combo.set(vehicle_data['trang_thai'])

        # Nút Lưu / Hủy
        button_frame = ttk.Frame(container)
        button_frame.grid(row=9, column=0, columnspan=2, pady=25, sticky="ew")
        ttk.Button(button_frame, text="💾 Lưu", bootstyle="success", command=self.save_vehicle).pack(side="left", expand=True, fill="x", padx=(0,5))
        ttk.Button(button_frame, text="❌ Hủy", bootstyle="secondary", command=self.destroy).pack(side="left", expand=True, fill="x", padx=(5,0))

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

    def load_driver_names(self):
        """Load danh sách tài xế từ DB."""
        try:
            drivers = self.db_model.get_all_drivers(status="Hoạt động")
            self.driver_map = {d[1]: d[0] for d in drivers}  # {name: ma_tai_xe}
            self.driver_combo['values'] = list(self.driver_map.keys())
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách tài xế: {e}")

    def save_vehicle(self):
        try:
            vehicle_id = self.vehicle_data['id_phuong_tien']
            driver_name = self.driver_combo.get().strip()
            driver_code = self.driver_map.get(driver_name, None)

            # Lấy biển số hiện tại từ vehicle_data vì không sửa được
            plate = self.vehicle_data['bien_so_xe']

            data = {
                'plate': plate,  # Gán biển số để tránh NULL
                'type': self.type_entry.get().strip(),
                'mileage': int(self.mileage_entry.get()),
                'last_maintenance': self.maintenance_entry.get_date().strftime("%Y-%m-%d"),
                'status': self.status_combo.get(),
                'driver_code': driver_code
            }

            # Kiểm tra biển số trùng (nếu muốn)
            if self.db_model.is_plate_exists(plate, exclude_vehicle_id=vehicle_id):
                messagebox.showerror("Lỗi", f"Biển số {plate} đã tồn tại!")
                return

            success = self.db_model.update_vehicle_by_id(vehicle_id, data)
            if success:
                messagebox.showinfo("Thành công", "Phương tiện đã được cập nhật.")
                self.destroy()
                if self.callback:
                    self.callback()
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật phương tiện.")

        except ValueError:
            messagebox.showerror("Lỗi", "Số km phải là một số nguyên.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật phương tiện: {e}")
