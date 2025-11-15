# models/vehicle_model.py
from .db_connect import Database
import mysql.connector


class VehicleModel:

    def get_all_vehicles(self, status=None, search=None):
        """
        Lấy tất cả phương tiện, JOIN với tài xế, có thể lọc/tìm kiếm.
        """
        db = None
        try:
            db = Database()
            # Câu query này JOIN 2 bảng
            query = """
                SELECT 
                    p.id_phuong_tien, 
                    p.bien_so_xe, 
                    p.loai_xe, 
                    p.so_km_da_di, 
                    p.ngay_bao_tri_cuoi, 
                    p.trang_thai, 
                    t.ho_ten -- Lấy tên tài xế
                FROM PhuongTien AS p
                LEFT JOIN TaiXe AS t 
                    ON p.ma_tai_xe_phu_trach = t.ma_tai_xe
            """

            params = []
            conditions = []

            # 1. Lọc theo Trạng thái
            if status:
                conditions.append("p.trang_thai = %s")
                params.append(status)

            # 2. Lọc theo Tìm kiếm
            if search:
                search_like = f"%{search}%"
                # Tìm theo Biển số HOẶC Loại xe
                conditions.append("(p.bien_so_xe LIKE %s OR p.loai_xe LIKE %s)")
                params.extend([search_like, search_like])

            # 3. Nối các điều kiện
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY p.id_phuong_tien"

            if params:
                return db.fetch_all(query, params)
            else:
                return db.fetch_all(query)

        except mysql.connector.Error as err:
            print(f"Lỗi khi lấy dữ liệu phương tiện: {err}")
            return []
        finally:
            if db:
                db.close()

    def get_vehicle_stats(self):
        """
        Lấy số liệu thống kê cho 3 thẻ trên trang Quản lý Phương Tiện.
        """
        db = None
        try:
            db = Database()

            query_total = "SELECT COUNT(*) FROM PhuongTien"
            total_count = db.fetch_one(query_total)[0]

            query_active = "SELECT COUNT(*) FROM PhuongTien WHERE trang_thai = 'Hoạt động'"
            active_count = db.fetch_one(query_active)[0]

            query_maintenance = "SELECT COUNT(*) FROM PhuongTien WHERE trang_thai = 'Bảo trì'"
            maintenance_count = db.fetch_one(query_maintenance)[0]

            return {
                "total": total_count or 0,
                "active": active_count or 0,
                "maintenance": maintenance_count or 0
            }

        except mysql.connector.Error as err:
            print(f"Lỗi khi lấy số liệu thống kê phương tiện: {err}")
            return {"total": 0, "active": 0, "maintenance": 0}
        finally:
            if db:
                db.close()

    # --- CÁC HÀM HỖ TRỢ CHO MODAL ---
    # (Dựa trên code `vehicle_page.py` của bạn)

    def get_available_drivers(self):
        """
        Lấy danh sách các tài xế 'Hoạt động' VÀ 'chưa được gán xe'.
        """
        db = None
        try:
            db = Database()
            # Lấy các tài xế hoạt động
            query_active_drivers = "SELECT ma_tai_xe, ho_ten FROM TaiXe WHERE trang_thai = 'Hoạt động'"
            active_drivers = db.fetch_all(query_active_drivers)

            # Lấy các tài xế đã được gán xe
            query_assigned_drivers = "SELECT ma_tai_xe_phu_trach FROM PhuongTien WHERE ma_tai_xe_phu_trach IS NOT NULL"
            assigned_list = [row[0] for row in db.fetch_all(query_assigned_drivers)]

            # Lọc ra những người chưa được gán
            available = [driver for driver in active_drivers if driver[0] not in assigned_list]
            return available

        except mysql.connector.Error as err:
            print(f"Lỗi khi lấy danh sách tài xế có sẵn: {err}")
            return []
        finally:
            if db:
                db.close()

    def get_driver_info(self, driver_code):
        """Lấy Mã và Tên của MỘT tài xế (dùng cho form Edit)."""
        db = None
        try:
            db = Database()
            query = "SELECT ma_tai_xe, ho_ten FROM TaiXe WHERE ma_tai_xe = %s"
            return db.fetch_one(query, (driver_code,))
        except mysql.connector.Error as err:
            print(f"Lỗi khi lấy thông tin tài xế {driver_code}: {err}")
            return None
        finally:
            if db:
                db.close()

    def is_plate_exists(self, plate, exclude_vehicle_id=None):
        """
        Kiểm tra biển số xe đã tồn tại chưa.
        Nếu có 'exclude_vehicle_id', bỏ qua ID đó (dùng khi EDIT).
        """
        db = None
        try:
            db = Database()
            query = "SELECT id_phuong_tien FROM PhuongTien WHERE bien_so_xe = %s"
            params = [plate]

            if exclude_vehicle_id:
                query += " AND id_phuong_tien != %s"
                params.append(exclude_vehicle_id)

            result = db.fetch_one(query, tuple(params))
            return result is not None  # True nếu tồn tại

        except mysql.connector.Error as err:
            print(f"Lỗi khi kiểm tra biển số: {err}")
            return True  # Mặc định là True để tránh lỗi
        finally:
            if db:
                db.close()

    def add_vehicle(self, data):
        """Thêm xe mới vào CSDL."""
        db = None
        try:
            db = Database()
            query = """
                INSERT INTO PhuongTien 
                (bien_so_xe, loai_xe, so_km_da_di, ngay_bao_tri_cuoi, trang_thai, ma_tai_xe_phu_trach) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                data['plate'],
                data['type'],
                data['mileage'],
                data['last_maintenance'],
                data['status'],
                data['driver_code']  # Có thể là None
            )
            db.execute_query(query, params)
            return True
        except mysql.connector.Error as err:
            print(f"Lỗi khi thêm phương tiện: {err}")
            return False
        finally:
            if db:
                db.close()

        # (Đây là code để bạn thay thế trong file models/vehicle_model.py)

    def get_vehicle_by_id(self, vehicle_id):
            """
            Lấy toàn bộ dữ liệu của 1 xe bằng ID (dạng dictionary).
            SỬA LẠI: Hàm này tự quản lý cursor để sửa lỗi AttributeError.
            """
            db = None  # Đây là đối tượng Database (quản lý kết nối)
            cursor = None  # Đây là con trỏ (cursor) thô
            try:
                db = Database()  # Tạo kết nối
                if not db.conn:
                    print("Lỗi: Không thể kết nối CSDL trong get_vehicle_by_id")
                    return None

                cursor = db.conn.cursor()  # Lấy một con trỏ (cursor) mới từ kết nối

                query = "SELECT * FROM PhuongTien WHERE id_phuong_tien = %s"
                cursor.execute(query, (vehicle_id,))
                result_tuple = cursor.fetchone()  # Lấy 1 dòng kết quả (dạng tuple)

                if result_tuple:
                    # Lấy tên các cột
                    column_names = [desc[0] for desc in cursor.description]
                    # Ghép tên cột và dữ liệu lại thành dictionary
                    return dict(zip(column_names, result_tuple))

                return None  # Nếu không tìm thấy

            except mysql.connector.Error as err:
                print(f"Lỗi khi lấy xe theo ID: {err}")
                return None
            finally:
                # Dọn dẹp
                if cursor:
                    cursor.close()  # Luôn đóng cursor
                if db:
                    db.close()  # Luôn đóng kết nối

    def update_vehicle_by_id(self, vehicle_id, data):
        """Cập nhật xe dựa trên ID."""
        db = None
        try:
            db = Database()
            query = """
                UPDATE PhuongTien SET
                    loai_xe = %s,
                    so_km_da_di = %s,
                    ngay_bao_tri_cuoi = %s,
                    trang_thai = %s,
                    ma_tai_xe_phu_trach = %s,
                    bien_so_xe = %s 
                WHERE 
                    id_phuong_tien = %s
            """
            params = (
                data['type'],
                data['mileage'],
                data['last_maintenance'],
                data['status'],
                data['driver_code'],
                data['plate'],  # Biển số xe (dù không sửa)
                vehicle_id
            )
            db.execute_query(query, params)
            return True
        except mysql.connector.Error as err:
            print(f"Lỗi khi cập nhật phương tiện {vehicle_id}: {err}")
            return False
        finally:
            if db:
                db.close()

    def delete_vehicle(self, plate):
        """Xóa xe dựa trên BIỂN SỐ XE."""
        db = None
        try:
            db = Database()
            query = "DELETE FROM PhuongTien WHERE bien_so_xe = %s"
            db.execute_query(query, (plate,))
            return True
        except mysql.connector.Error as err:
            print(f"Lỗi khi xóa phương tiện {plate}: {err}")
            return False
        finally:
            if db:
                db.close()