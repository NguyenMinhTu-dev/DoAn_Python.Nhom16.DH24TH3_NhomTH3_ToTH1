# views/trip_page.py
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# === IMPORT MODEL ===
try:
    from models.trip_model import TripModel
except ImportError as e:
    print(f"Lỗi Import trong trip_page: {e}")

# Định nghĩa màu sắc
COLOR_PRIMARY_TEAL = "#00A79E"
COLOR_ORANGE = "#fd7e14"
COLOR_BLUE = "#17a2b8"
COLOR_RED = "#dc3545"


class TripPage(ttk.Frame):
    """Trang Giao diện Quản lý Chuyến xe & Hóa đơn"""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.configure(padding=(20, 10))

        # === KHỞI TẠO MODEL ===
        try:
            self.db_model = TripModel()
        except Exception as e:
            print(f"Không thể khởi tạo TripModel: {e}")
            self.db_model = None

        # --- 1. Tiêu đề ---
        title_frame = ttk.Frame(self, style="TFrame")
        title_frame.pack(fill="x", anchor="n", pady=(0, 10))

        left_title_frame = ttk.Frame(title_frame, style="TFrame")
        left_title_frame.pack(side="left", fill="x", expand=True)

        ttk.Label(left_title_frame, text="Quản Lý Chuyến Xe & Hóa Đơn",
                  font=("Arial", 24, "bold"),
                  style="TLabel").pack(anchor="w")
        ttk.Label(left_title_frame, text="Xem lịch sử chuyến xe, doanh thu và các hóa đơn.",
                  style="secondary.TLabel").pack(anchor="w")

        # Nút "Thêm Chuyến" bị ẩn/xóa, vì logic này thường từ app người dùng

        # --- 2. Hàng Thống Kê ---
        stat_frame = ttk.Frame(self, style="TFrame")
        stat_frame.pack(fill="x", expand=True, pady=10)

        card1 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(card1, text="Tổng Doanh Thu", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        self.revenue_label = ttk.Label(card1, text="0 đ", font=("Arial", 22, "bold"),
                                       style="light.TLabel", foreground=COLOR_PRIMARY_TEAL)
        self.revenue_label.pack(anchor="w", pady=5)
        ttk.Label(card1, text="Doanh thu từ các chuyến đã hoàn thành", bootstyle="success").pack(anchor="w")

        card2 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card2.pack(side="left", fill="x", expand=True, padx=10)
        ttk.Label(card2, text="Chuyến Hoàn Thành", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        self.completed_label = ttk.Label(card2, text="0", font=("Arial", 22, "bold"),
                                         style="light.TLabel", foreground=COLOR_BLUE)
        self.completed_label.pack(anchor="w", pady=5)
        ttk.Label(card2, text="Tổng số chuyến đã thanh toán", bootstyle="info").pack(anchor="w")

        card3 = ttk.Frame(stat_frame, bootstyle="light", padding=20)
        card3.pack(side="left", fill="x", expand=True, padx=(10, 0))
        ttk.Label(card3, text="Chuyến Đang Diễn Ra", font=("Arial", 12), style="light.TLabel").pack(anchor="w")
        self.active_label = ttk.Label(card3, text="0", font=("Arial", 22, "bold"),
                                      style="light.TLabel", foreground=COLOR_ORANGE)
        self.active_label.pack(anchor="w", pady=5)
        ttk.Label(card3, text="Các chuyến chưa kết thúc", bootstyle="warning").pack(anchor="w")

        # --- 3. Notebook (Tabs) ---
        notebook = ttk.Notebook(self)
        notebook.pack(fill="x", pady=10)

        tab_all = ttk.Frame(notebook)
        tab_completed = ttk.Frame(notebook)
        tab_active = ttk.Frame(notebook)
        tab_cancelled = ttk.Frame(notebook)

        notebook.add(tab_all, text="  Tất Cả  ")
        notebook.add(tab_completed, text="  Hoàn thành  ")
        notebook.add(tab_active, text="  Đang diễn ra  ")
        notebook.add(tab_cancelled, text="  Đã hủy  ")

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        # --- 4. Thanh hành động ---
        action_bar = ttk.Frame(self, style="TFrame")
        action_bar.pack(fill="x", pady=5)

        self.details_button = ttk.Button(action_bar, text="Xem Chi Tiết",
                                         bootstyle="outline-info",
                                         state="disabled",
                                         command=self.open_details_modal)
        self.details_button.pack(side="left", padx=(0, 5))

        self.cancel_button = ttk.Button(action_bar, text="Hủy Chuyến",
                                        bootstyle="outline-danger",
                                        state="disabled",
                                        command=self.cancel_selected_trip)
        self.cancel_button.pack(side="left", padx=5)

        search_entry = ttk.Entry(action_bar, width=50)
        search_entry.pack(side="right", fill="x", expand=True)
        search_entry.insert(0, "Tìm mã chuyến, tên khách, SĐT tài xế...")

        # --- 5. Bảng Dữ Liệu (Treeview) ---
        table_container = ttk.Frame(self, style="TFrame")
        table_container.pack(fill="both", expand=True, pady=10)

        # Cột dựa trên query JOIN của model
        columns = ("id", "customer_name", "driver_name", "license_plate", "destination", "total_cost", "status")

        self.tree = ttk.Treeview(table_container,
                                 columns=columns,
                                 show='tree headings',
                                 height=15)

        self.tree.heading("#0", text=" ")
        self.tree.column("#0", width=40, anchor="center")

        self.tree.heading("id", text="Mã Chuyến")
        self.tree.column("id", width=80, anchor="center")
        self.tree.heading("customer_name", text="Tên Khách Hàng")
        self.tree.column("customer_name", width=180)
        self.tree.heading("driver_name", text="Tên Tài Xế")
        self.tree.column("driver_name", width=180)
        self.tree.heading("license_plate", text="Biển Số Xe")
        self.tree.column("license_plate", width=100, anchor="center")
        self.tree.heading("destination", text="Điểm Đến")
        self.tree.column("destination", width=200)
        self.tree.heading("total_cost", text="Tổng Tiền (VND)")
        self.tree.column("total_cost", width=120, anchor="e")  # Căn lề phải
        self.tree.heading("status", text="Trạng Thái")
        self.tree.column("status", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Cấu hình Tags màu
        self.tree.tag_configure('hoanthanh', foreground='#28a745')  # Green
        self.tree.tag_configure('dangdienra', foreground='#fd7e14')  # Orange
        self.tree.tag_configure('dahuy', foreground='#dc3545')  # Red

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.bind("<Button-1>", self.deselect_tree)
        action_bar.bind("<Button-1>", self.deselect_tree)

        # --- 6. Phân trang ---
        pagination_frame = ttk.Frame(self, style="TFrame")
        pagination_frame.pack(fill="x", pady=(10, 0))
        self.pagination_label = ttk.Label(pagination_frame, text="Đang tải...", style="secondary.TLabel")
        self.pagination_label.pack(side="left")

        # --- 7. Tải dữ liệu lần đầu ---
        self.load_stats()
        self.load_data_into_tree(filter_status=None)

    def load_stats(self):
        """Tải số liệu thống kê từ model và cập nhật các card."""
        if not self.db_model:
            return
        try:
            stats = self.db_model.get_stats()
            self.revenue_label.config(text=f"{stats['revenue']:,.0f} đ")
            self.completed_label.config(text=f"{stats['completed']}")
            self.active_label.config(text=f"{stats['active']}")
        except Exception as e:
            print(f"Lỗi tải stats: {e}")

    def on_tab_selected(self, event):
        """Được gọi khi người dùng nhấp vào một tab"""
        selected_tab_text = event.widget.tab(event.widget.select(), "text").strip()
        self.tree.selection_set()

        if selected_tab_text == "Tất Cả":
            self.load_data_into_tree(filter_status=None)
        elif selected_tab_text == "Hoàn thành":
            self.load_data_into_tree(filter_status="Hoàn thành")
        elif selected_tab_text == "Đang diễn ra":
            self.load_data_into_tree(filter_status="Đang diễn ra")
        elif selected_tab_text == "Đã hủy":
            self.load_data_into_tree(filter_status="Đã hủy")

    def load_data_into_tree(self, filter_status=None):
        """Xóa bảng và tải lại dữ liệu dựa trên trạng thái lọc"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.db_model:
            return

        try:
            trip_data = self.db_model.get_all_trips_for_view(status=filter_status)
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu chuyến xe: {e}")
            trip_data = []

        tag_map = {
            "Hoàn thành": "hoanthanh",
            "Đang diễn ra": "dangdienra",
            "Đã hủy": "dahuy"
        }

        count = 0
        for item in trip_data:
            # item là tuple: (id, ten_kh, ten_tx, bien_so, diem_den, tong_tien, trang_thai)

            # Định dạng lại tiền tệ
            formatted_item = list(item)
            formatted_item[5] = f"{item[5]:,.0f}"  # Cột tổng tiền

            status_value = item[-1]
            status_tag = tag_map.get(status_value, "")

            self.tree.insert("", "end", values=formatted_item, tags=(status_tag,))
            count += 1

        self.pagination_label.config(text=f"Hiển thị {count} trong {count} kết quả.")

    def on_tree_select(self, event):
        """Kích hoạt nút Sửa/Xóa khi một dòng được chọn."""
        selected = self.tree.selection()
        if not selected:
            self.details_button.config(state="disabled")
            self.cancel_button.config(state="disabled")
            return

        self.details_button.config(state="enabled")

        # Chỉ cho phép Hủy nếu chuyến "Đang diễn ra"
        item = self.tree.item(selected[0])
        status = item['values'][-1]  # Lấy trạng thái

        if status == "Đang diễn ra":
            self.cancel_button.config(state="enabled")
        else:
            self.cancel_button.config(state="disabled")

    def deselect_tree(self, event):
        """Bỏ chọn tất cả các dòng khi nhấp ra ngoài."""
        if not self.tree.identify_region(event.x, event.y) == "heading":
            if not self.tree.focus():
                self.tree.selection_set()

    def open_details_modal(self):
        """Mở cửa sổ Toplevel để XEM CHI TIẾT chuyến đi."""
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        trip_id = item['values'][0]  # Mã Chuyến

        if not self.db_model:
            messagebox.showerror("Lỗi", "Model chưa kết nối.")
            return

        # Lấy chi tiết đầy đủ từ model
        details = self.db_model.get_trip_details(trip_id)

        if details:
            ViewTripModal(self, details)
        else:
            messagebox.showerror("Lỗi", f"Không thể tìm thấy chi tiết cho chuyến xe {trip_id}.")

    def cancel_selected_trip(self):
        """Hủy chuyến xe đang được chọn (nếu đang diễn ra)."""
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        trip_id = item['values'][0]

        if messagebox.askyesno("Xác nhận Hủy",
                               f"Bạn có chắc muốn HỦY chuyến xe {trip_id}?\nChuyến xe sẽ được chuyển sang trạng thái 'Đã hủy'."):
            if not self.db_model:
                messagebox.showerror("Lỗi", "Model chưa kết nối.")
                return

            success = self.db_model.update_trip_status(trip_id, "Đã hủy")
            if success:
                messagebox.showinfo("Thành công", f"Đã hủy chuyến xe {trip_id}.")
                self.load_data_into_tree(filter_status="Đang diễn ra")  # Tải lại tab hiện tại
                self.load_stats()  # Cập nhật lại thẻ thống kê
            else:
                messagebox.showerror("Lỗi", "Không thể hủy chuyến xe (có thể chuyến đã kết thúc).")


# ===================================================================
# === LỚP MODAL: XEM CHI TIẾT (VIEW-ONLY) ===
# ===================================================================
class ViewTripModal(tk.Toplevel):
    def __init__(self, parent, details_tuple):
        super().__init__(parent)

        # Chuyển tuple sang dict cho dễ đọc code
        # Dựa trên query: SELECT c.*, kh.ho_ten, kh.sdt, tx.ho_ten, tx.sdt
        details = {
            "id_chuyen_xe": details_tuple[0],
            "id_khach_hang": details_tuple[1],
            "ma_tai_xe": details_tuple[2],
            "bien_so_xe": details_tuple[3],
            "diem_don": details_tuple[4],
            "diem_den": details_tuple[5],
            "so_km": details_tuple[6],
            "thoi_gian_dat_xe": details_tuple[7],
            "thoi_gian_ket_thuc": details_tuple[8],
            "tong_tien": details_tuple[9],
            "phuong_thuc_thanh_toan": details_tuple[10],
            "trang_thai_chuyen_xe": details_tuple[11],
            "danh_gia_chuyen_xe": details_tuple[12],
            "ten_khach_hang": details_tuple[13],
            "sdt_khach_hang": details_tuple[14],
            "ten_tai_xe": details_tuple[15],
            "sdt_tai_xe": details_tuple[16],
        }

        self.title(f"Chi Tiết Chuyến Xe #{details['id_chuyen_xe']}")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        main_frame = ttk.Frame(self, padding=30, style='light')
        main_frame.pack(fill="both", expand=True)

        header_frame = ttk.Frame(main_frame, style='light')
        header_frame.pack(fill="x")

        ttk.Label(header_frame, text=f"Chi Tiết Chuyến Xe #{details['id_chuyen_xe']}", font=("Arial", 16, "bold"),
                  foreground=COLOR_PRIMARY_TEAL).pack(anchor="w")

        # Thêm trạng thái
        status = details['trang_thai_chuyen_xe']
        if status == "Hoàn thành":
            style = "success"
        elif status == "Đang diễn ra":
            style = "warning"
        elif status == "Đã hủy":
            style = "danger"
        else:
            style = "secondary"

        ttk.Label(header_frame, text=f"Trạng thái: {status}", bootstyle=style).pack(anchor="w", pady=(0, 20))

        self.create_details_widgets(main_frame, details)

        button_frame = ttk.Frame(main_frame, style='light')
        button_frame.pack(fill="x", pady=(20, 0))
        ttk.Button(button_frame, text="Đóng", command=self.destroy, bootstyle="secondary-outline").pack(side="right")

    def create_details_widgets(self, parent, details):
        form_frame = ttk.Frame(parent, style='light')
        form_frame.pack(fill="x")
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        # Hàm helper để tạo label
        def create_detail_entry(label, value, row, col):
            ttk.Label(form_frame, text=label, font=("Arial", 10, "bold")).grid(row=row, column=col, sticky="w",
                                                                               padx=(0, 10))

            # Dùng Label thay vì Entry vì đây là view-only
            val_label = ttk.Label(form_frame, text=value, font=("Arial", 11), style='light', wraplength=300)
            val_label.grid(row=row + 1, column=col, columnspan=2, sticky="w", pady=(2, 10))

        # --- CỘT 1: THÔNG TIN KHÁCH HÀNG & TÀI XẾ ---
        create_detail_entry("Khách Hàng:", f"{details['ten_khach_hang']} ({details['sdt_khach_hang']})", 0, 0)
        create_detail_entry("Tài Xế:", f"{details['ten_tai_xe']} ({details['sdt_tai_xe']})", 2, 0)
        create_detail_entry("Biển Số Xe:", details['bien_so_xe'], 4, 0)

        # --- CỘT 2: THÔNG TIN TÀI CHÍNH ---
        create_detail_entry("Tổng Tiền:", f"{details['tong_tien']:,.0f} VND", 0, 2)
        create_detail_entry("Thanh Toán:", details['phuong_thuc_thanh_toan'], 2, 2)
        create_detail_entry("Đánh Giá:", f"{details['danh_gia_chuyen_xe']} sao" if details[
            'danh_gia_chuyen_xe'] else "Chưa đánh giá", 4, 2)

        # --- HÀNG 3: ĐỊA ĐIỂM (Full width) ---
        ttk.Label(form_frame, text="Điểm Đón", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=4,
                                                                                sticky="w", pady=(10, 0))
        ttk.Label(form_frame, text=details['diem_don'], font=("Arial", 11), style='light', wraplength=600).grid(row=7,
                                                                                                                column=0,
                                                                                                                columnspan=4,
                                                                                                                sticky="w",
                                                                                                                pady=(2,
                                                                                                                      10))

        ttk.Label(form_frame, text="Điểm Đến", font=("Arial", 10, "bold")).grid(row=8, column=0, columnspan=4,
                                                                                sticky="w", pady=(10, 0))
        ttk.Label(form_frame, text=details['diem_den'], font=("Arial", 11), style='light', wraplength=600).grid(row=9,
                                                                                                                column=0,
                                                                                                                columnspan=4,
                                                                                                                sticky="w",
                                                                                                                pady=(2,
                                                                                                                      10))

        # --- HÀNG 4: THỜI GIAN (Tách 2 cột) ---
        create_detail_entry("Thời Gian Đặt:", details['thoi_gian_dat_xe'], 10, 0)
        create_detail_entry("Thời Gian Kết Thúc:", details['thoi_gian_ket_thuc'] or "Chưa kết thúc", 10, 2)