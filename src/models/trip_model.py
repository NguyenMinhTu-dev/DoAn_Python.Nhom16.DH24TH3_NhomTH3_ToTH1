# models/trip_model.py
from .db_connect import Database
import mysql.connector


class TripModel:

    def get_all_trips_for_view(self, status=None, search=None):
        """
        Lấy dữ liệu các chuyến xe, JOIN với KhachHang và TaiXe,
        có thể lọc theo TRẠNG THÁI và TÌM KIẾM.
        """
        db = None
        try:
            db = Database()

            query = """
                SELECT 
                    c.id_chuyen_xe,
                    kh.ho_ten AS ten_khach_hang,
                    tx.ho_ten AS ten_tai_xe,
                    c.bien_so_xe,
                    c.diem_den,
                    c.tong_tien,
                    c.trang_thai_chuyen_xe
                FROM 
                    ChuyenXe AS c
                JOIN 
                    KhachHang AS kh ON c.id_khach_hang = kh.id_khach_hang
                JOIN 
                    TaiXe AS tx ON c.ma_tai_xe = tx.ma_tai_xe
            """

            params = []
            conditions = []  # Dùng để nối các điều kiện WHERE

            # 1. Xử lý lọc theo Trạng thái (status)
            if status:
                conditions.append("c.trang_thai_chuyen_xe = %s")
                params.append(status)

            # 2. Xử lý lọc theo Tìm kiếm (search)
            if search:
                search_like = f"%{search}%"
                # Tìm kiếm ở 4 cột: Mã Chuyến, Tên KH, Tên TX, Biển Số
                conditions.append("""
                    (c.id_chuyen_xe LIKE %s OR 
                     kh.ho_ten LIKE %s OR 
                     tx.ho_ten LIKE %s OR
                     c.bien_so_xe LIKE %s)
                """)
                params.extend([search_like, search_like, search_like, search_like])

            # 3. Nối các điều kiện lại
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY c.thoi_gian_dat_xe DESC"  # Sắp xếp chuyến mới nhất lên đầu

            if params:
                return db.fetch_all(query, params)
            else:
                return db.fetch_all(query)

        except mysql.connector.Error as err:
            print(f"Lỗi khi lấy dữ liệu Chuyến Xe (view): {err}")
            return []
        finally:
            if db:
                db.close()

    def get_trip_details(self, trip_id):
        """
        Lấy TẤT CẢ thông tin chi tiết của MỘT chuyến xe để hiển thị modal.
        """
        db = None
        try:
            db = Database()
            query = """
                SELECT 
                    c.*, 
                    kh.ho_ten AS ten_khach_hang, 
                    kh.so_dien_thoai AS sdt_khach_hang,
                    tx.ho_ten AS ten_tai_xe,
                    tx.so_dien_thoai AS sdt_tai_xe
                FROM 
                    ChuyenXe AS c
                JOIN 
                    KhachHang AS kh ON c.id_khach_hang = kh.id_khach_hang
                JOIN 
                    TaiXe AS tx ON c.ma_tai_xe = tx.ma_tai_xe
                WHERE 
                    c.id_chuyen_xe = %s
            """
            params = (trip_id,)
            return db.fetch_one(query, params)

        except mysql.connector.Error as err:
            print(f"Lỗi khi lấy chi tiết chuyến xe {trip_id}: {err}")
            return None
        finally:
            if db:
                db.close()

    def update_trip_status(self, trip_id, new_status):
        """
        Cập nhật trạng thái của một chuyến xe (ví dụ: 'Đã hủy').
        """
        db = None
        try:
            db = Database()
            query = """
                UPDATE ChuyenXe 
                SET trang_thai_chuyen_xe = %s 
                WHERE id_chuyen_xe = %s
            """
            params = (new_status, trip_id)

            # Chỉ cho phép hủy nếu chuyến đang diễn ra
            if new_status == 'Đã hủy':
                query += " AND trang_thai_chuyen_xe = 'Đang diễn ra'"

            db.execute_query(query, params)

            if db.cursor.rowcount > 0:
                return True
            else:
                return False

        except mysql.connector.Error as err:
            print(f"Lỗi khi cập nhật trạng thái chuyến xe {trip_id}: {err}")
            return False
        finally:
            if db:
                db.close()

    def get_stats(self):
        """
        Lấy 3 số liệu thống kê cho thẻ card.
        """
        db = None
        try:
            db = Database()

            # 1. Tổng doanh thu (chỉ tính chuyến 'Hoàn thành')
            query_revenue = "SELECT SUM(tong_tien) FROM ChuyenXe WHERE trang_thai_chuyen_xe = 'Hoàn thành'"
            revenue = db.fetch_one(query_revenue)[0]

            # 2. Số chuyến hoàn thành
            query_completed = "SELECT COUNT(*) FROM ChuyenXe WHERE trang_thai_chuyen_xe = 'Hoàn thành'"
            completed_count = db.fetch_one(query_completed)[0]

            # 3. Số chuyến đang diễn ra
            query_active = "SELECT COUNT(*) FROM ChuyenXe WHERE trang_thai_chuyen_xe = 'Đang diễn ra'"
            active_count = db.fetch_one(query_active)[0]

            return {
                "revenue": revenue or 0,  # Trả về 0 nếu None
                "completed": completed_count or 0,
                "active": active_count or 0
            }

        except mysql.connector.Error as err:
            print(f"Lỗi khi lấy số liệu thống kê: {err}")
            return {"revenue": 0, "completed": 0, "active": 0}
        finally:
            if db:
                db.close()