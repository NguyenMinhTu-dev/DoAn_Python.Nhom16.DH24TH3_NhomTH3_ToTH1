from gui.Login import LoginApp
from gui.main_window import MainWindowApp
from tkinter import messagebox
# Import model xử lý logic đăng nhập
from models.user_model import verify_login


class AppController:
    def __init__(self, root):
        self.root = root
        self.login_window = None
        self.main_window = None

        # Bắt đầu bằng việc hiển thị cửa sổ đăng nhập
        self.show_login_window()

    def show_login_window(self):
        """Hiển thị cửa sổ đăng nhập."""
        if self.main_window:
            self.main_window.destroy()
            self.main_window = None

        # Tạo cửa sổ Toplevel mới cho Đăng nhập
        self.login_window = LoginApp(self.root, controller=self)
        self.login_window.grab_set()  # Giữ focus

    def show_main_window(self, user_info):
        """Hiển thị cửa sổ chính sau khi đăng nhập thành công."""
        if self.login_window:
            self.login_window.destroy()  # Đóng cửa sổ đăng nhập
            self.login_window = None

        # Hiển thị lại cửa sổ gốc (đã bị ẩn) để làm cửa sổ chính
        self.root.deiconify()
        self.main_window = MainWindowApp(self.root, controller=self, user_info=user_info)

    def _handle_login(self, username, password, role_value):
        """
        Xử lý logic đăng nhập khi người dùng nhấn nút.
        ĐƯỢC GỌI TỪ Login.py
        """
        # 1. Gọi model để xác minh
        login_result = verify_login(username, password)

        if login_result:
            vai_tro, user_id = login_result

            # 2. Kiểm tra vai trò người dùng chọn (trên GUI) có khớp với CSDL không
            role_selected = "Khách hàng" if role_value == 1 else "Tài xế"

            if vai_tro == role_selected:
                # 3. Đăng nhập thành công và đúng vai trò
                user_info = {'id': user_id, 'role': vai_tro}
                self.show_main_window(user_info)
            else:
                # 4. Mật khẩu đúng, nhưng chọn sai vai trò
                messagebox.showerror("Lỗi", f"Tài khoản này là tài khoản '{vai_tro}', không phải '{role_selected}'.")

        else:
            # 5. Sai tài khoản hoặc mật khẩu
            messagebox.showerror("Lỗi", "Tài khoản (Email/SĐT) hoặc Mật khẩu không đúng.")

    def _handle_logout(self):
        """
        Xử lý đăng xuất.
        ĐƯỢC GỌI TỪ main_window.py
        """
        # Ẩn cửa sổ chính
        self.root.withdraw()
        self.show_login_window()