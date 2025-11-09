import customtkinter as ctk
from app_controller import AppController
import sys
import os

# Thêm thư mục 'src' vào sys.path để Python có thể tìm thấy các mô-đun
# (quan trọng khi chạy từ thư mục gốc DoAn/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Đi lên 1 cấp (từ src ra DoAn) rồi thêm src vào
sys.path.append(os.path.dirname(current_dir))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Cấu hình giao diện chung
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Ẩn cửa sổ gốc (chỉ là trình quản lý)
        self.withdraw()

        # Khởi chạy bộ điều khiển chính
        self.controller = AppController(self)


if __name__ == "__main__":
    # Đảm bảo các file .env và CSDL đã được thiết lập
    app = App()
    app.mainloop()