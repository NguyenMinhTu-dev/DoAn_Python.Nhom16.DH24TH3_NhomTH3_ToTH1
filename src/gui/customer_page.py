import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# === IMPORT MODEL ===
try:
    from models.customer_model import CustomerModel
except ImportError as e:
    print(f"Lỗi Import trong customer_page: {e}")

# Định nghĩa màu sắc
COLOR_PRIMARY_TEAL = "#00A79E"


class CustomerPage(ttk.Frame):
    """Trang Giao diện Quản lý Khách Hàng"""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.configure(padding=(20, 10))

        # === KHỞI TẠO MODEL ===
        try:
            self.db_model = CustomerModel()
        except Exception as e:
            print(f"Không thể khởi tạo CustomerModel: {e}")
            self.db_model = None

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
                                bootstyle="success",
                                command=self.open_add_customer_modal)
        add_button.pack(side="right", anchor="ne", pady=10)

        # --- 2. Hàng Thống Kê ---
        stat_frame = ttk.Frame(self, style="TFrame")
        stat_frame.pack(fill="x", expand=True, pady=10)

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

        # --- 4. Thanh hành động ---
        action_bar = ttk.Frame(self, style="TFrame")
        action_bar.pack(fill="x", pady=5)

        self.edit_button = ttk.Button(action_bar, text="Sửa",
                                      bootstyle="outline-warning",
                                      state="disabled",
                                      command=self.open_edit_customer_modal)
        self.edit_button.pack(side="left", padx=(0, 5))

        self.delete_button = ttk.Button(action_bar, text="Xóa",
                                        bootstyle="outline-danger",
                                        state="disabled",
                                        command=self.delete_selected_customer)
        self.delete_button.pack(side="left", padx=5)

        search_entry = ttk.Entry(action_bar, width=50)
        search_entry.pack(side="right", fill="x", expand=True)
        search_entry.insert(0, "Tìm theo mã KH, tên, SĐT...")

        # --- 5. Bảng Dữ Liệu (Treeview) ---
        table_container = ttk.Frame(self, style="TFrame")
        table_container.pack(fill="both", expand=True, pady=10)

        columns = ("id", "name", "phone", "email", "rank")

        self.tree = ttk.Treeview(table_container,
                                 columns=columns,
                                 show='tree headings',
                                 height=15)

        self.tree.heading("#0", text=" ")
        self.tree.column("#0", width=50, anchor="center")

        self.tree.heading("id", text="Mã Khách Hàng")
        self.tree.column("id", width=120, anchor="center")
        self.tree.heading("name", text="Họ Tên")
        self.tree.column("name", width=200)
        self.tree.heading("phone", text="Số Điện Thoại")
        self.tree.column("phone", width=150, anchor="center")
        self.tree.heading("email", text="Email")
        self.tree.column("email", width=200)
        self.tree.heading("rank", text="Hạng")
        self.tree.column("rank", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Tags màu sắc
        self.tree.tag_configure('vip', foreground='#fd7e14')  # Cam
        self.tree.tag_configure('bac', foreground='#6c757d')  # Xám
        self.tree.tag_configure('dong', foreground='#17a2b8')  # Xanh lơ

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.bind("<Button-1>", self.deselect_tree)
        action_bar.bind("<Button-1>", self.deselect_tree)

        # --- 6. Phân trang ---
        pagination_frame = ttk.Frame(self, style="TFrame")
        pagination_frame.pack(fill="x", pady=(10, 0))
        self.pagination_label = ttk.Label(pagination_frame, text="Đang tải...", style="secondary.TLabel")
        self.pagination_label.pack(side="left")

        # Tải dữ liệu lần đầu
        self.load_data_into_tree(filter_status=None)

    def open_add_customer_modal(self):
        if self.db_model:
            AddCustomerModal(self, self.db_model, callback=lambda: self.load_data_into_tree())
        else:
            messagebox.showerror("Lỗi", "Model chưa kết nối.")

    def delete_selected_customer(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        customer_code = item['values'][0]
        customer_name = item['values'][1]

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa khách hàng {customer_name}?"):
            success = self.db_model.delete_customer(customer_code)
            if success:
                messagebox.showinfo("Thành công", "Đã xóa khách hàng.")
                self.load_data_into_tree()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa khách hàng.")

    def open_edit_customer_modal(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        customer_code = item['values'][0]

        EditCustomerModal(self, self.db_model, customer_code, callback=lambda: self.load_data_into_tree())

    def on_tab_selected(self, event):
        selected_tab_text = event.widget.tab(event.widget.select(), "text").strip()
        self.tree.selection_set()

        if selected_tab_text == "Tất Cả":
            self.load_data_into_tree(filter_status=None)
        elif selected_tab_text == "VIP":
            self.load_data_into_tree(filter_status="VIP")
        elif selected_tab_text == "Bạc":
            self.load_data_into_tree(filter_status="Bạc")
        elif selected_tab_text == "Đồng":
            self.load_data_into_tree(filter_status="Đồng")

    def load_data_into_tree(self, filter_status=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.db_model:
            return

        try:
            customer_data = self.db_model.get_all_customers(rank=filter_status)
        except Exception as e:
            print(f"Lỗi data: {e}")
            customer_data = []

        tag_map = {"VIP": "vip", "Bạc": "bac", "Đồng": "dong"}
        count = 0
        for item in customer_data:
            status_value = item[-1]  # Cột Rank nằm cuối
            status_tag = tag_map.get(status_value, "")
            self.tree.insert("", "end", values=item, tags=(status_tag,))
            count += 1

        self.pagination_label.config(text=f"Hiển thị {count} kết quả.")

    def on_tree_select(self, event):
        if self.tree.selection():
            self.edit_button.config(state="enabled")
            self.delete_button.config(state="enabled")
        else:
            self.edit_button.config(state="disabled")
            self.delete_button.config(state="disabled")

    def deselect_tree(self, event):
        if not self.tree.identify_region(event.x, event.y) == "heading":
            if not self.tree.focus():
                self.tree.selection_set()


class AddCustomerModal(tk.Toplevel):
    def __init__(self, parent, db_model, callback=None):
        tk.Toplevel.__init__(self, parent)
        self.title("Thêm Khách Hàng Mới")
        self.db_model = db_model
        self.callback = callback
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        main_frame = ttk.Frame(self, padding=30, style='light')
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Thêm Khách Hàng", font=("Arial", 16, "bold"),
                  foreground=COLOR_PRIMARY_TEAL).pack(pady=(0, 10))

        self.create_form_widgets(main_frame)

        button_frame = ttk.Frame(main_frame, style='light')
        button_frame.pack(fill="x", pady=20)
        ttk.Button(button_frame, text="Lưu", command=self.save_customer, bootstyle="success").pack(side="right")
        ttk.Button(button_frame, text="Hủy", command=self.destroy, bootstyle="secondary-outline").pack(side="right",
                                                                                                       padx=10)

    def create_form_widgets(self, parent):
        form_frame = ttk.Frame(parent, style='light')
        form_frame.pack(fill="x")
        form_frame.columnconfigure(1, weight=1)

        # Họ Tên
        ttk.Label(form_frame, text="Họ Tên", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w",
                                                                              pady=(10, 0))
        self.name_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 10), ipady=5)

        # Email
        ttk.Label(form_frame, text="Email", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.email_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.email_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10), ipady=5)

        # SĐT
        ttk.Label(form_frame, text="Số Điện Thoại", font=("Arial", 10, "bold")).grid(row=2, column=1, sticky="w",
                                                                                     pady=(10, 0))
        self.phone_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.phone_entry.grid(row=3, column=1, sticky="ew", padx=(10, 0), ipady=5)

        # Hạng
        ttk.Label(form_frame, text="Hạng Thành Viên", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2,
                                                                                       sticky="w", pady=(10, 0))
        self.rank_combo = ttk.Combobox(form_frame, values=["Đồng", "Bạc", "VIP"], state="readonly")
        self.rank_combo.set("Đồng")
        self.rank_combo.grid(row=5, column=0, columnspan=2, sticky="ew", padx=(0, 10), ipady=5)

    def save_customer(self):
        data = {
            'name': self.name_entry.get(),
            'email': self.email_entry.get(),
            'phone': self.phone_entry.get(),
            'rank': self.rank_combo.get()
        }
        if not data['name'] or not data['phone']:
            messagebox.showerror("Lỗi", "Vui lòng nhập Họ tên và SĐT.")
            return

        if self.db_model.add_customer(data):
            messagebox.showinfo("Thành công", "Đã thêm khách hàng.")
            self.destroy()
            if self.callback: self.callback()
        else:
            messagebox.showerror("Lỗi", "Lỗi khi lưu vào CSDL.")


class EditCustomerModal(tk.Toplevel):
    def __init__(self, parent, db_model, customer_code, callback=None):
        super().__init__(parent)
        self.db_model = db_model
        self.customer_code = customer_code
        self.callback = callback
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        main_frame = ttk.Frame(self, padding=30, style='light')
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Sửa Thông Tin", font=("Arial", 16, "bold"),
                  foreground=COLOR_PRIMARY_TEAL).pack(pady=(0, 10))

        all_data = self.db_model.get_all_customers()
        customer_data = next((d for d in all_data if d[0] == customer_code), None)

        self.create_form_widgets(main_frame, customer_data)

        button_frame = ttk.Frame(main_frame, style='light')
        button_frame.pack(fill="x", pady=20)
        ttk.Button(button_frame, text="Lưu", command=self.save_customer, bootstyle="success").pack(side="right")
        ttk.Button(button_frame, text="Hủy", command=self.destroy, bootstyle="secondary-outline").pack(side="right",
                                                                                                       padx=10)

    def create_form_widgets(self, parent, data):
        form_frame = ttk.Frame(parent, style='light')
        form_frame.pack(fill="x")
        form_frame.columnconfigure(1, weight=1)

        # Họ Tên
        ttk.Label(form_frame, text="Họ Tên", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w",
                                                                              pady=(10, 0))
        self.name_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 10), ipady=5)
        if data: self.name_entry.insert(0, data[1])

        # Email
        ttk.Label(form_frame, text="Email", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.email_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.email_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10), ipady=5)
        if data: self.email_entry.insert(0, data[3])

        # SĐT
        ttk.Label(form_frame, text="Số Điện Thoại", font=("Arial", 10, "bold")).grid(row=2, column=1, sticky="w",
                                                                                     pady=(10, 0))
        self.phone_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.phone_entry.grid(row=3, column=1, sticky="ew", padx=(10, 0), ipady=5)
        if data: self.phone_entry.insert(0, data[2])

        # Hạng
        ttk.Label(form_frame, text="Hạng Thành Viên", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2,
                                                                                       sticky="w", pady=(10, 0))
        self.rank_combo = ttk.Combobox(form_frame, values=["Đồng", "Bạc", "VIP"], state="readonly")
        self.rank_combo.grid(row=5, column=0, columnspan=2, sticky="ew", padx=(0, 10), ipady=5)
        if data: self.rank_combo.set(data[4])

    def save_customer(self):
        data = {
            'name': self.name_entry.get(),
            'email': self.email_entry.get(),
            'phone': self.phone_entry.get(),
            'rank': self.rank_combo.get()
        }
        if self.db_model.update_customer(self.customer_code, data):
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin.")
            self.destroy()
            if self.callback: self.callback()
        else:
            messagebox.showerror("Lỗi", "Không thể cập nhật.")