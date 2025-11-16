import mysql.connector
import hashlib

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '11022005',
    'database': 'QLXEVALAIXE'
}


class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            # SỬA: Xóa bỏ self.cursor khỏi __init__
            # self.cursor = self.conn.cursor() # <-- DÒNG NÀY GÂY LỖI
            print("Kết nối MySQL thành công!")
        except mysql.connector.Error as err:
            print(f"Lỗi kết nối MySQL: {err}")
            self.conn = None
            # self.cursor = None

    def fetch_all(self, query, params=None):
        if not self.conn: return []
        cursor = None  # SỬA: Tạo cursor mới
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Lỗi truy vấn (fetch_all): {err}")
            return []
        finally:
            if cursor:
                cursor.close()  # SỬA: Đóng cursor

    def fetch_one(self, query, params=None):
        if not self.conn: return None
        cursor = None  # SỬA: Tạo cursor mới
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Lỗi truy vấn (fetch_one): {err}")
            return None
        finally:
            if cursor:
                cursor.close()  # SỬA: Đóng cursor

    def execute_query(self, query, params=None):
        if not self.conn: return False
        cursor = None  # SỬA: Tạo cursor mới
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Lỗi truy vấn (execute): {err}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()  # SỬA: Đóng cursor

    def check_login(self, username, password):
        """Kiểm tra đăng nhập bằng cách hash mật khẩu và so sánh"""
        if not self.conn: return False

        # SỬA: CSDL của bạn dùng MD5 (cho '123'), không phải SHA256
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

        query = "SELECT * FROM `TaiKhoanQuanTri` WHERE `ten_dang_nhap` = %s AND `mat_khau_hash` = %s"

        # SỬA: Hàm fetch_one bây giờ đã an toàn,
        # nó sẽ tự tạo và đóng cursor
        result = self.fetch_one(query, (username, password_hash))

        return result is not None

    def get_dashboard_stats(self):
        """Lấy các số liệu cho trang Dashboard"""
        try:
            stats = {}
            # SỬA: Các hàm fetch_one này giờ đã an toàn
            stats['total_drivers'] = self.fetch_one("SELECT COUNT(*) FROM `TaiXe`")[0]
            stats['total_customers'] = self.fetch_one("SELECT COUNT(*) FROM `KhachHang`")[0]
            stats['total_vehicles'] = self.fetch_one("SELECT COUNT(*) FROM `PhuongTien`")[0]

            # (Bạn có thể bỏ comment dòng này nếu có bảng ChuyenDi)
            # stats['total_trips_month'] = self.fetch_one("SELECT COUNT(*) FROM `ChuyenDi` WHERE MONTH(ngay_khoi_hanh) = MONTH(CURRENT_DATE())")[0]

            stats['total_trips_month'] = 1500  # Số mẫu

            return stats
        except Exception as e:
            print(f"Lỗi lấy thông số Dashboard: {e}")
            return {'total_drivers': 0, 'total_customers': 0, 'total_vehicles': 0, 'total_trips_month': 0}

    # === CÁC HÀM LẤY DỮ LIỆU CHO TỪNG TRANG ===
    # (Lưu ý: các hàm này có thể cần sửa lại để nhận 'search_term'
    #  nếu bạn muốn dùng chức năng tìm kiếm)

    def get_drivers(self, status=None):
        query = "SELECT `ma_tai_xe`, `ho_ten`, `hang_xe_lai`, `so_bang_lai`, `email`, `so_dien_thoai`, `danh_gia_trung_binh`, `trang_thai` FROM `TaiXe`"
        if status:
            query += " WHERE `trang_thai` = %s"
            return self.fetch_all(query, (status,))
        return self.fetch_all(query)

    def get_vehicles(self, status=None):
        query = "SELECT `bien_so_xe`, `loai_xe`, `ma_tai_xe_phu_trach`, `so_km_da_di`, `ngay_bao_tri_cuoi`, `trang_thai` FROM `PhuongTien`"
        if status:
            query += " WHERE `trang_thai` = %s"
            return self.fetch_all(query, (status,))
        return self.fetch_all(query)

    def get_customers(self, rank=None):
        # SỬA: Xóa cột `hang_thanh_vien` bị lặp
        query = "SELECT `id_khach_hang`, `ho_ten`, `so_dien_thoai`, `email`, `hang_thanh_vien` FROM `KhachHang`"
        if rank:
            query += " WHERE `hang_thanh_vien` = %s"
            return self.fetch_all(query, (rank,))
        return self.fetch_all(query)

    def close(self):
        if self.conn:
            # SỬA: Xóa self.cursor.close()
            self.conn.close()
            print("Đã đóng kết nối MySQL.")