import mysql.connector
import hashlib

# THAY THẾ CÁC THÔNG SỐ NÀY BẰNG THÔNG SỐ CỦA BẠN
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '11022005',  # <-- THAY MẬT KHẨU CỦA BẠN VÀO ĐÂY
    'database': 'QLXEVALAIXE'  # Tên database tiếng Việt
}


class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            print("Kết nối MySQL thành công!")
        except mysql.connector.Error as err:
            print(f"Lỗi kết nối MySQL: {err}")
            self.conn = None
            self.cursor = None

    def fetch_all(self, query, params=None):
        if not self.conn: return []
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Lỗi truy vấn (fetch_all): {err}")
            return []

    def fetch_one(self, query, params=None):
        if not self.conn: return None
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Lỗi truy vấn (fetch_one): {err}")
            return None

    def execute_query(self, query, params=None):
        if not self.conn: return False
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Lỗi truy vấn (execute): {err}")
            self.conn.rollback()
            return False

    def check_login(self, username, password):
        """Kiểm tra đăng nhập bằng cách hash mật khẩu và so sánh"""
        if not self.conn: return False

        # Hash mật khẩu (giống như trong file .sql)
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        query = "SELECT * FROM `TaiKhoanQuanTri` WHERE `ten_dang_nhap` = %s AND `mat_khau_hash` = %s"
        result = self.fetch_one(query, (username, password_hash))

        return result is not None

    def get_dashboard_stats(self):
        """Lấy các số liệu cho trang Dashboard"""
        try:
            stats = {}
            # (Bạn có thể sửa các câu query này để lọc theo tháng, v.v.)
            stats['total_drivers'] = self.fetch_one("SELECT COUNT(*) FROM `TaiXe`")[0]
            stats['total_customers'] = self.fetch_one("SELECT COUNT(*) FROM `KhachHang`")[0]
            stats['total_vehicles'] = self.fetch_one("SELECT COUNT(*) FROM `PhuongTien`")[0]
            # (Giả sử bạn đã thêm lại bảng ChuyenDi)
            # stats['total_trips_month'] = self.fetch_one("SELECT COUNT(*) FROM `ChuyenDi` WHERE MONTH(ngay_khoi_hanh) = MONTH(CURRENT_DATE())")[0]

            # Thay thế bằng các số mẫu nếu chưa có bảng ChuyenDi
            stats['total_trips_month'] = 1500  # Số mẫu

            return stats
        except Exception as e:
            print(f"Lỗi lấy thông số Dashboard: {e}")
            return {'total_drivers': 0, 'total_customers': 0, 'total_vehicles': 0, 'total_trips_month': 0}

    # === CÁC HÀM LẤY DỮ LIỆU CHO TỪNG TRANG ===
    # (Tên cột phải khớp với file .sql tiếng Việt)

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
        query = "SELECT `id_khach_hang`, `ho_ten`, `so_dien_thoai`, `email`, `hang_thanh_vien`, `hang_thanh_vien` FROM `KhachHang`"  # Cột cuối là 'rank'
        if rank:
            query += " WHERE `hang_thanh_vien` = %s"
            return self.fetch_all(query, (rank,))
        return self.fetch_all(query)

    # (Nếu bạn dùng lại trang Chuyến Đi, đây là code cho nó)
    # def get_trips(self, status=None):
    #     query = "SELECT ..."
    #     if status:
    #         ...
    #     return self.fetch_all(query)

    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Đã đóng kết nối MySQL.")