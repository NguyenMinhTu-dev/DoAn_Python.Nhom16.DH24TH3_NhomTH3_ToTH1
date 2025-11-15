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
                                style="Primary.TButton",
                                command=self.open_add_vehicle_modal)

        add_button.pack(side="right", anchor="ne", pady=10)

        # --- 2. Hàng Thống Kê (SỬA ĐỔI) ---
        stat_frame = ttk.Frame(self, style="TFrame")
        stat_frame.pack(fill="x", expand=True, pady=10)

        # Card 1: Tổng Số Phương Tiện
        card1 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(card1, text="Tổng Số Phương Tiện", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        # SỬA: Gán self, bỏ màu
        self.total_label = ttk.Label(card1, text="Đang tải...", font=("Arial", 22, "bold"),
                                     style="light.TLabel")
        self.total_label.pack(anchor="w", pady=5)
        self.total_sublabel = ttk.Label(card1, text=" ", bootstyle="success")
        self.total_sublabel.pack(anchor="w")

        # Card 2: Đang Hoạt Động
        card2 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card2.pack(side="left", fill="x", expand=True, padx=10)
        ttk.Label(card2, text="Đang Hoạt Động", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        # SỬA: Gán self, bỏ màu
        self.active_label = ttk.Label(card2, text="Đang tải...", font=("Arial", 22, "bold"),
                                      style="light.TLabel")
        self.active_label.pack(anchor="w", pady=5)
        self.active_sublabel = ttk.Label(card2, text=" ", bootstyle="info")
        self.active_sublabel.pack(anchor="w")

        # Card 3: Đang Bảo Trì
        card3 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card3.pack(side="left", fill="x", expand=True, padx=(10, 0))
        ttk.Label(card3, text="Đang Bảo Trì", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        # SỬA: Gán self, bỏ màu
        self.maintenance_label = ttk.Label(card3, text="Đang tải...", font=("Arial", 22, "bold"),
                                           style="light.TLabel")
        self.maintenance_label.pack(anchor="w", pady=5)
        self.maintenance_sublabel = ttk.Label(card3, text=" ", bootstyle="warning")
        self.maintenance_sublabel.pack(anchor="w")

        # --- 3. Notebook (Tabs) ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="x", pady=10)

        tab_all = ttk.Frame(self.notebook)
        tab_active = ttk.Frame(self.notebook)
        tab_maintenance = ttk.Frame(self.notebook)
        tab_stopped = ttk.Frame(self.notebook)

        self.notebook.add(tab_all, text="  Tất Cả  ")
        self.notebook.add(tab_active, text="  Đang Hoạt Động  ")
        self.notebook.add(tab_maintenance, text="  Bảo Trì  ")
        self.notebook.add(tab_stopped, text="  Ngừng Hoạt Động  ")

        # SỬA: Bind sự kiện để gọi hàm tìm kiếm/lọc
        self.notebook.bind("<<NotebookTabChanged>>", self.perform_filter_and_search)

        # --- 4. Thanh hành động (Sửa, Xóa, Tìm kiếm) ---
        action_bar = ttk.Frame(self, style="TFrame")
        action_bar.pack(fill="x", pady=5)

        self.edit_button = ttk.Button(action_bar, text="Sửa",
                                      bootstyle="outline-warning",
                                      state="disabled",
                                      command=self.open_edit_vehicle_modal)
        self.edit_button.pack(side="left", padx=(0, 5))

        self.delete_button = ttk.Button(action_bar, text="Xóa",
                                        bootstyle="outline-danger",
                                        state="disabled",
                                        command=self.delete_selected_vehicle)
        self.delete_button.pack(side="left", padx=5)

        # --- SỬA: Chức năng Tìm Kiếm ---
        self.search_placeholder = "Tìm theo biển số xe, loại xe..."
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
        columns = ("id_vehicle", "plate", "type", "mileage", "last_maintenance", "status", "driver_name")
        self.tree = ttk.Treeview(table_container, columns=columns, show='tree headings', height=15)
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
        self.tree.heading("driver_name", text="Tài Xế Phụ Trách")  # Sửa: Lấy tên
        self.tree.column("driver_name", width=150)  # Sửa: Tăng độ rộng
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
        elif selected_tab_text == "Bảo Trì":
            filter_status = "Bảo trì"
        elif selected_tab_text == "Ngừng Hoạt Động":
            filter_status = "Ngừng hoạt động"

        self.load_data_into_tree(filter_status=filter_status, search_term=search_term)

    # === HÀM MỚI: Tải số liệu thống kê ===
    def load_stats(self):
        if not self.db_model:
            return
        try:
            # 1. Gọi model (Giả định model có hàm get_vehicle_stats())
            stats = self.db_model.get_vehicle_stats()

            total = stats.get('total', 0)
            active = stats.get('active', 0)
            maintenance = stats.get('maintenance', 0)

            # 2. Cập nhật các Label chính
            self.total_label.config(text=f"{total:,.0f}")
            self.active_label.config(text=f"{active:,.0f}")
            self.maintenance_label.config(text=f"{maintenance:,.0f}")

            # 3. Cập nhật các Label phụ (tính %)
            active_percent = (active / total * 100) if total > 0 else 0
            maintenance_percent = (maintenance / total * 100) if total > 0 else 0

            self.total_sublabel.config(text="Tổng số xe trong hệ thống")
            self.active_sublabel.config(text=f"{active_percent:.1f}% tổng số xe")
            self.maintenance_sublabel.config(text=f"{maintenance_percent:.1f}% tổng số xe")

        except Exception as e:
            print(f"Lỗi khi tải số liệu phương tiện: {e}")
            self.total_label.config(text="Lỗi")
            self.active_label.config(text="Lỗi")
            self.maintenance_label.config(text="Lỗi")

    # === HÀM MỚI: Dùng để làm mới từ bên ngoài ===
    def refresh_data(self):
        """
        Hàm public mà file app.py chính sẽ gọi mỗi khi trang này được hiển thị.
        """
        print("Đang làm mới dữ liệu VehiclePage...")
        self.load_stats()  # Tải các thẻ thống kê

        self.search_entry.delete(0, "end")
        self.on_search_focus_out(None)
        self.notebook.select(0)  # Chọn tab "Tất Cả"
        self.load_data_into_tree(filter_status=None, search_term="")  # Tải lại bảng
        self.tree.selection_set()  # Bỏ chọn

    def open_add_vehicle_modal(self):
        if self.db_model:
            # SỬA: Gọi refresh_data()
            AddVehicleModal(self, self.db_model, callback=self.refresh_data)
        else:
            messagebox.showerror("Lỗi", "Không thể mở form thêm xe vì Model chưa kết nối.")

    def open_edit_vehicle_modal(self):
        selected = self.tree.selection()
        if not selected: return

        item = self.tree.item(selected[0])
        vehicle_id = item['values'][0]

        vehicle_data = self.db_model.get_vehicle_by_id(vehicle_id)
        if not vehicle_data:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu phương tiện.")
            return

        # SỬA: Gọi refresh_data()
        EditVehicleModal(self, self.db_model, vehicle_data, callback=self.refresh_data)

    def delete_selected_vehicle(self):
        selected = self.tree.selection()
        if not selected: return

        item = self.tree.item(selected[0])
        plate = item['values'][1]

        if not plate:
            messagebox.showerror("Lỗi", "Biển số xe không hợp lệ.")
            return

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa phương tiện {plate}?"):
            success = self.db_model.delete_vehicle(plate)
            if success:
                messagebox.showinfo("Thành công", f"Đã xóa phương tiện {plate}.")
                self.refresh_data()  # SỬA: Gọi refresh_data()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa phương tiện.")

    def on_tab_selected(self, event):
        # SỬA: Hàm này giờ chỉ cần gọi hàm tổng
        self.perform_filter_and_search(event)

    # SỬA: load_data_into_tree giờ nhận cả search_term
    def load_data_into_tree(self, filter_status=None, search_term=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.db_model:
            ttk.Label(self, text="Lỗi: Không thể kết nối Model.", bootstyle="danger").pack()
            return

        if search_term == self.search_placeholder:
            search_term = None

        try:
            # SỬA: Truyền cả hai tham số cho model
            vehicle_data = self.db_model.get_all_vehicles(status=filter_status, search=search_term)
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
            # SỬA: Định dạng lại dữ liệu trước khi chèn
            # Dữ liệu từ model: (id, bien_so, loai_xe, so_km, ngay_bao_tri, trang_thai, ten_tai_xe)

            # 1. Mã Xe
            id_vehicle = item[0]
            # 2. Biển số
            plate = item[1]
            # 3. Loại xe
            type_v = item[2]
            # 4. Số Km (định dạng 120,500)
            mileage = f"{item[3]:,}"
            # 5. Ngày bảo trì (định dạng dd/mm/YYYY)
            last_maintenance = item[4]
            if isinstance(last_maintenance, datetime.date):
                last_maintenance = last_maintenance.strftime("%d/%m/%Y")
            elif not last_maintenance:
                last_maintenance = "Chưa có"
            # 6. Trạng thái
            status_value = item[5]
            # 7. Tên tài xế (có thể là None)
            driver_name = item[6] if item[6] else "Chưa gán"

            data_values = (id_vehicle, plate, type_v, mileage, last_maintenance, status_value, driver_name)

            status_tag = tag_map.get(status_value, "")
            self.tree.insert("", "end", text="", values=data_values, tags=(status_tag,))
            count += 1

        # SỬA: Sửa lỗi pagination
        self.pagination_label.config(text=f"Hiển thị {count} trong {count} kết quả.")

    def on_tree_select(self, event):
        if self.tree.selection():
            self.edit_button.config(state="enabled")
            self.delete_button.config(state="enabled")
        else:
            self.edit_button.config(state="disabled")
            self.delete_button.config(state="disabled")  # Sửa: tắt cả nút xóa

    def deselect_tree(self, event):
        if not self.tree.identify_region(event.x, event.y) == "heading":
            if not self.tree.focus():
                self.tree.selection_set()

    # === FORM THÊM/SỬA XE ===


# (Các lớp AddVehicleModal và EditVehicleModal giữ nguyên)
# (Vui lòng giữ nguyên code của 2 class này)
class AddVehicleModal(tk.Toplevel):
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

        ttk.Label(container, text="Thêm Xe Mới", font=("Arial", 16, "bold")).grid(
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

        # Mapping: tên -> mã
        self.driver_map = {}
        self.load_driver_names()

        # Trạng thái
        ttk.Label(container, text="Trạng thái:").grid(row=7, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.status_combo = ttk.Combobox(container, values=["Hoạt động", "Bảo trì", "Ngừng hoạt động"],
                                         state="readonly")
        self.status_combo.grid(row=8, column=0, columnspan=2, sticky="ew", pady=2)
        self.status_combo.current(0)

        # Nút Lưu / Hủy
        button_frame = ttk.Frame(container)
        button_frame.grid(row=9, column=0, columnspan=2, pady=25, sticky="ew")
        ttk.Button(button_frame, text="Lưu", bootstyle="success", command=self.save_vehicle).pack(
            side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(button_frame, text="Hủy", bootstyle="secondary", command=self.destroy).pack(
            side="left", expand=True, fill="x", padx=(5, 0))

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

    def load_driver_names(self):
        """Load danh sách tài xế (chỉ những người đang Hoạt động và CHƯA có xe)"""
        try:
            # Sửa: Cần hàm get_available_drivers()
            drivers = self.db_model.get_available_drivers()
            names = [f"{driver[0]} - {driver[1]}" for driver in drivers]  # "TX001 - Nguyễn Văn An"
            self.driver_combo['values'] = ["Không gán"] + names  # Thêm tùy chọn không gán

            # Mapping: "TX001 - Nguyễn Văn An" -> "TX001"
            self.driver_map = {f"{driver[0]} - {driver[1]}": driver[0] for driver in drivers}
            self.driver_map["Không gán"] = None

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách tài xế: {e}", parent=self)
            self.driver_map = {"Không gán": None}
            self.driver_combo['values'] = ["Không gán"]

    def save_vehicle(self):
        try:
            plate = self.plate_entry.get().strip().upper()  # Viết hoa biển số
            if not plate:
                messagebox.showerror("Lỗi", "Vui lòng nhập biển số xe.", parent=self)
                return

            if self.db_model.is_plate_exists(plate):
                messagebox.showerror("Lỗi", f"Biển số {plate} đã tồn tại!", parent=self)
                return

            driver_name_full = self.driver_combo.get().strip()
            driver_code = self.driver_map.get(driver_name_full, None)

            data = {
                'plate': plate,
                'type': self.type_entry.get(),
                'mileage': int(self.mileage_entry.get() or 0),
                'last_maintenance': self.maintenance_entry.get_date().strftime("%Y-%m-%d"),
                'status': self.status_combo.get(),
                'driver_code': driver_code
            }

            success = self.db_model.add_vehicle(data)
            if success:
                messagebox.showinfo("Thành công", "Xe mới đã được thêm.", parent=self)
                self.destroy()
                if self.callback:
                    self.callback()
            else:
                messagebox.showerror("Lỗi", "Không thể thêm xe (Lỗi CSDL).", parent=self)

        except ValueError:
            messagebox.showerror("Lỗi", "Số km phải là một số nguyên.", parent=self)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm xe: {e}", parent=self)


class EditVehicleModal(tk.Toplevel):
    def __init__(self, parent, db_model, vehicle_data, callback=None):
        super().__init__(parent)
        self.parent = parent
        self.db_model = db_model
        self.vehicle_data = vehicle_data  # Đây là Dữ liệu đầy đủ (dict)
        self.callback = callback

        self.title("Sửa Phương Tiện")
        self.geometry("520x500")
        self.resizable(False, False)

        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Sửa Phương Tiện", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 15)
        )

        # Biển số xe (Không cho sửa, vì là khóa chính)
        ttk.Label(container, text="Biển số xe:").grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.plate_entry = ttk.Entry(container, width=22, state="normal")
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

        self.driver_map = {}
        self.current_driver_code = vehicle_data.get('ma_tai_xe_phu_trach')
        self.load_driver_names_for_edit()

        # Trạng thái
        ttk.Label(container, text="Trạng thái:").grid(row=7, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.status_combo = ttk.Combobox(container, values=["Hoạt động", "Bảo trì", "Ngừng hoạt động"],
                                         state="readonly")
        self.status_combo.grid(row=8, column=0, columnspan=2, sticky="ew", pady=2)
        self.status_combo.set(vehicle_data['trang_thai'])

        # Nút Lưu / Hủy
        button_frame = ttk.Frame(container)
        button_frame.grid(row=9, column=0, columnspan=2, pady=25, sticky="ew")
        ttk.Button(button_frame, text="Lưu", bootstyle="success", command=self.save_vehicle).pack(side="left",
                                                                                                  expand=True, fill="x",
                                                                                                  padx=(0, 5))
        ttk.Button(button_frame, text="Hủy", bootstyle="secondary", command=self.destroy).pack(side="left", expand=True,
                                                                                               fill="x", padx=(5, 0))

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

    def load_driver_names_for_edit(self):
        """
        Tải danh sách tài xế, BAO GỒM cả tài xế hiện tại của xe này.
        """
        try:
            # Lấy tất cả tài xế chưa có xe
            available_drivers = self.db_model.get_available_drivers()
            # { "TX001": "TX001 - Nguyễn Văn An", ...}
            self.driver_map = {d[0]: f"{d[0]} - {d[1]}" for d in available_drivers}

            # Lấy thông tin tài xế hiện tại (nếu có)
            current_driver_name = "Không gán"
            if self.current_driver_code:
                # Kiểm tra xem tài xế hiện tại có trong ds có sẵn ko
                if self.current_driver_code not in self.driver_map:
                    # Nếu không, lấy thông tin của tài xế đó
                    driver_info = self.db_model.get_driver_info(self.current_driver_code)  # Cần hàm này
                    if driver_info:
                        self.driver_map[driver_info[0]] = f"{driver_info[0]} - {driver_info[1]}"

                current_driver_name = self.driver_map.get(self.current_driver_code, "Không gán")

            # Nạp vào combobox
            driver_list = ["Không gán"] + list(self.driver_map.values())
            self.driver_combo['values'] = driver_list
            self.driver_combo.set(current_driver_name)

            # Đảo ngược map để lưu: { "TX001 - Nguyễn Văn An": "TX001" }
            self.driver_map_reversed = {v: k for k, v in self.driver_map.items()}
            self.driver_map_reversed["Không gán"] = None

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách tài xế: {e}", parent=self)
            self.driver_map_reversed = {"Không gán": None}
            self.driver_combo['values'] = ["Không gán"]
            self.driver_combo.set("Không gán")

    def save_vehicle(self):
        try:
            vehicle_id = self.vehicle_data['id_phuong_tien']

            driver_name_full = self.driver_combo.get().strip()
            driver_code = self.driver_map_reversed.get(driver_name_full, None)

            # === SỬA LỖI MẤT BIỂN SỐ ===
            # Lấy biển số từ dữ liệu gốc (self.vehicle_data)
            # thay vì từ ô entry (vì ô đó bị 'disabled')
            #plate = self.vehicle_data['bien_so_xe']
            plate = self.plate_entry.get().strip().upper()
            # ==========================

            data = {
                'plate': plate,  # <-- Bây giờ đã đúng
                'type': self.type_entry.get().strip(),
                'mileage': int(self.mileage_entry.get()),
                'last_maintenance': self.maintenance_entry.get_date().strftime("%Y-%m-%d"),
                'status': self.status_combo.get(),
                'driver_code': driver_code
            }

            success = self.db_model.update_vehicle_by_id(vehicle_id, data)
            if success:
                messagebox.showinfo("Thành công", "Phương tiện đã được cập nhật.", parent=self)
                self.destroy()
                if self.callback:
                    self.callback()
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật phương tiện.", parent=self)

        except ValueError:
            messagebox.showerror("Lỗi", "Số km phải là một số nguyên.", parent=self)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật phương tiện: {e}", parent=self)