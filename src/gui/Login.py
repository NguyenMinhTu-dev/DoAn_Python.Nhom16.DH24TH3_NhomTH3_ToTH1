import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import subprocess  # Thư viện để mở file khác
import sys  # Thư viện để tìm đường dẫn python
import os

# --- 1. Cấu hình & Biến toàn cục ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLOR_PRIMARY = "#20B2AA"
COLOR_TEXT_DARK = "#29313D"

recaptcha_verified = False
current_captcha_number = 0


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Cấu hình Form Đăng nhập ---
        self.title("Xanh SM - Đăng nhập")
        self.geometry("600x600")
        self.configure(fg_color=COLOR_PRIMARY)
        self.resizable(False, False)

        # Đặt cửa sổ ở giữa màn hình
        self.eval('tk::PlaceWindow . center')

        # --- Khung trắng trung tâm ---
        login_frame = ctk.CTkFrame(self, width=400, height=500, corner_radius=10, fg_color="white")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        login_frame.grid_columnconfigure(0, weight=1)

        # --- Các thành phần của Form ---
        logo_label = ctk.CTkLabel(login_frame, text="✔", font=ctk.CTkFont(size=30, weight="bold"),
                                  text_color=COLOR_PRIMARY)
        logo_label.grid(row=0, column=0, pady=(30, 0), padx=50, sticky="n")

        title_label = ctk.CTkLabel(login_frame, text="Xanh SM", font=ctk.CTkFont(size=24, weight="bold"),
                                   text_color=COLOR_PRIMARY)
        title_label.grid(row=1, column=0, pady=(0, 0), sticky="n")

        subtitle_label = ctk.CTkLabel(login_frame, text="Đăng nhập vào hệ thống", font=ctk.CTkFont(size=10),
                                      text_color="gray")
        subtitle_label.grid(row=2, column=0, pady=(0, 20), sticky="n")

        # Vai trò
        role_label = ctk.CTkLabel(login_frame, text="Đăng nhập với tư cách", font=ctk.CTkFont(size=10, weight="bold"),
                                  text_color=COLOR_TEXT_DARK)
        role_label.grid(row=3, column=0, padx=50, pady=(10, 5), sticky="w")

        self.role_var = tk.IntVar(value=1)
        role_frame = ctk.CTkFrame(login_frame, fg_color="white")
        role_frame.grid(row=4, column=0, padx=50, sticky="w")

        ctk.CTkRadioButton(role_frame, text="Khách hàng", variable=self.role_var, value=1, fg_color=COLOR_PRIMARY,
                           hover_color=COLOR_PRIMARY).pack(side="left", padx=(0, 15))
        ctk.CTkRadioButton(role_frame, text="Tài xế", variable=self.role_var, value=2, fg_color=COLOR_PRIMARY,
                           hover_color=COLOR_PRIMARY).pack(side="left")

        # Tài khoản
        ctk.CTkLabel(login_frame, text="Tài khoản", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=COLOR_TEXT_DARK).grid(row=5, column=0, padx=50, pady=(20, 5), sticky="w")
        self.account_entry = ctk.CTkEntry(login_frame, width=300, placeholder_text="Nhập tài khoản")
        self.account_entry.grid(row=6, column=0, padx=50, sticky="ew")

        # Mật khẩu
        ctk.CTkLabel(login_frame, text="Mật khẩu", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=COLOR_TEXT_DARK).grid(row=7, column=0, padx=50, pady=(20, 5), sticky="w")
        self.password_entry = ctk.CTkEntry(login_frame, width=300, show="*", placeholder_text="Nhập mật khẩu")
        self.password_entry.grid(row=8, column=0, padx=50, sticky="ew")

        # reCAPTCHA
        self.recaptcha_var = tk.IntVar(value=0)
        self.recaptcha_checkbutton = ctk.CTkCheckBox(login_frame,
                                                     text="Tôi không phải robot",
                                                     variable=self.recaptcha_var,
                                                     command=self.handle_recaptcha_check,
                                                     hover_color=COLOR_PRIMARY,
                                                     fg_color=COLOR_PRIMARY)
        self.recaptcha_checkbutton.grid(row=9, column=0, padx=50, pady=(20, 10), sticky="w")

        # Nút Đăng nhập
        login_button = ctk.CTkButton(login_frame, text="Đăng nhập", command=self._login_attempt,
                                     fg_color=COLOR_PRIMARY, hover_color="#1A9E96",
                                     font=ctk.CTkFont(size=14, weight="bold"))
        login_button.grid(row=10, column=0, padx=50, pady=(10, 30), sticky="ew")

    def generate_and_show_captcha(self):
        global current_captcha_number, recaptcha_verified
        current_captcha_number = random.randint(1000, 9999)

        dialog = ctk.CTkInputDialog(text=f"Vui lòng nhập số sau:\n\n{current_captcha_number}",
                                    title="Xác minh Bạn không phải Robot")

        user_input = dialog.get_input()

        if user_input is not None:
            try:
                user_input_int = int(user_input)
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")
                self.update_recaptcha_status(False)
                return

            if user_input_int == current_captcha_number:
                recaptcha_verified = True
                self.update_recaptcha_status(True)
                messagebox.showinfo("Thành công", "Xác minh hoàn tất! Bạn có thể đăng nhập.")
            else:
                recaptcha_verified = False
                messagebox.showerror("Lỗi", "Số xác minh không đúng. Vui lòng thử lại.")
                self.update_recaptcha_status(False)
        else:
            self.update_recaptcha_status(False)

    def handle_recaptcha_check(self):
        global recaptcha_verified

        if self.recaptcha_var.get() == 1 and not recaptcha_verified:
            self.recaptcha_var.set(0)
            self.generate_and_show_captcha()

        elif self.recaptcha_var.get() == 0:
            recaptcha_verified = False
            self.update_recaptcha_status(False)

    def update_recaptcha_status(self, verified: bool):
        global recaptcha_verified
        recaptcha_verified = verified
        self.recaptcha_var.set(1 if verified else 0)

        if verified:
            self.recaptcha_checkbutton.configure(text="Tôi không phải robot (Đã xác minh)")
        else:
            self.recaptcha_checkbutton.configure(text="Tôi không phải robot")

    def _login_attempt(self):
        global recaptcha_verified

        if not recaptcha_verified:
            messagebox.showwarning("Cảnh báo", "Vui lòng xác minh 'Tôi không phải robot' trước khi đăng nhập.")
            return

        account = self.account_entry.get()
        password = self.password_entry.get()

        # (Để thử nghiệm, sử dụng: admin / 123)
        if account == "admin" and password == "123":
            self.open_main_window()
        else:
            messagebox.showerror("Lỗi", "Tài khoản hoặc Mật khẩu không đúng.")

    def open_main_window(self):
        # Lấy đường dẫn đến trình thông dịch Python hiện tại
        python_executable = sys.executable

        # Lấy thư mục của file login.py hiện tại
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Tạo đường dẫn đầy đủ đến file main_window.py
        # (Vì nó nằm CÙNG THƯ MỤC với login.py)
        main_window_path = os.path.join(current_dir, "main_window.py")

        # Sử dụng đường dẫn đầy đủ
        subprocess.Popen([python_executable, main_window_path])

        # Đóng cửa sổ đăng nhập
        self.destroy()


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()