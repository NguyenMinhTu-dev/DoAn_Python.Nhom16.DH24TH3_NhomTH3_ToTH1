import hashlib
from .db_connect import Database
import mysql.connector


def check_login_credentials(username, password):
    """
    Kiểm tra thông tin đăng nhập trong bảng TaiKhoanQuanTri.
    Hàm này tự động hash mật khẩu người dùng nhập (password) sang MD5
    trước khi so sánh với CSDL.
    """
    db = None
    try:
        # 1. Hash mật khẩu người dùng nhập (ví dụ: '123') sang MD5
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

        db = Database()

        # 2. Truy vấn CSDL bằng mật khẩu đã hash
        # Sửa lỗi: Cần dùng backtick (`) cho tên cột Tiếng Việt
        query = "SELECT * FROM `TaiKhoanQuanTri` WHERE `ten_dang_nhap` = %s AND `mat_khau_hash` = %s"
        params = (username, hashed_password)  # <-- Dùng mật khẩu đã hash

        # fetch_one sẽ trả về 1 hàng (tuple) nếu tìm thấy, hoặc None nếu không
        result = db.fetch_one(query, params)

        if result:
            return True  # Đăng nhập thành công
        else:
            return False  # Sai tên đăng nhập hoặc mật khẩu

    except mysql.connector.Error as err:
        print(f"Lỗi khi kiểm tra đăng nhập (user_model): {err}")
        return False
    finally:
        if db:
            db.close()