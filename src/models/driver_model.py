from .db_connect import Database
import mysql.connector
from tkinter import messagebox  # Cần để hiển thị lỗi DB


class DriverModel:

    # (Đây là code để bạn chép vào file models/driver_model.py)
    # (Giả sử bạn đã import Database và mysql.connector)

    def get_all_drivers(self, status=None, search=None):
        """
        Lấy tất cả tài xế, có thể lọc theo TRẠNG THÁI và TÌM KIẾM.
        """
        db = None
        try:
            db = Database()
            # Câu query này phải khớp với các cột CSDL của bạn
            # Cột Treeview: (id, name, vehicle_category, license, email, phone, rating, status)
            # Cột CSDL: (ma_tai_xe, ho_ten, hang_xe_lai, so_bang_lai, email, so_dien_thoai, danh_gia_trung_binh, trang_thai)
            query = """
                    SELECT 
                        ma_tai_xe, 
                        ho_ten, 
                        hang_xe_lai, 
                        so_bang_lai, 
                        email, 
                        so_dien_thoai, 
                        danh_gia_trung_binh, 
                        trang_thai 
                    FROM TaiXe
                """

            params = []
            conditions = []  # Dùng để nối các điều kiện WHERE

            # 1. Xử lý lọc theo Trạng thái (status)
            if status:
                conditions.append("trang_thai = %s")
                params.append(status)

            # 2. Xử lý lọc theo Tìm kiếm (search)
            if search:
                search_like = f"%{search}%"
                # Tìm kiếm ở 3 cột: Mã, Tên, SĐT
                conditions.append("""
                        (ma_tai_xe LIKE %s OR 
                         ho_ten LIKE %s OR 
                         so_dien_thoai LIKE %s)
                    """)
                params.extend([search_like, search_like, search_like])

            # 3. Nối các điều kiện lại
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY ma_tai_xe"

            if params:
                return db.fetch_all(query, params)
            else:
                return db.fetch_all(query)

        except mysql.connector.Error as err:
            print(f"Lỗi khi lấy dữ liệu Tài xế: {err}")
            return []
        finally:
            if db:
                db.close()

    def get_driver_stats(self):
        """
        Lấy số liệu thống kê cho 3 thẻ trên trang Quản lý Tài Xế.
        """
        db = None
        try:
            db = Database()

            # 1. Đếm tổng số tài xế
            query_total = "SELECT COUNT(*) FROM TaiXe"
            total_count = db.fetch_one(query_total)[0]

            # 2. Đếm tài xế hoạt động
            query_active = "SELECT COUNT(*) FROM TaiXe WHERE trang_thai = 'Hoạt động'"
            active_count = db.fetch_one(query_active)[0]

            # 3. Đếm tài xế không hoạt động (Tạm ngưng + Chờ duyệt)
            query_inactive = "SELECT COUNT(*) FROM TaiXe WHERE trang_thai != 'Hoạt động'"
            inactive_count = db.fetch_one(query_inactive)[0]

            return {
                "total": total_count or 0,
                "active": active_count or 0,
                "inactive": inactive_count or 0
            }

        except mysql.connector.Error as err:
            print(f"Lỗi khi lấy số liệu thống kê tài xế: {err}")
            return {"total": 0, "active": 0, "inactive": 0}
        finally:
            if db:
                db.close()

        # (Đây là code để bạn thay thế trong models/driver_model.py)
    def add_driver(self, data):
            """Thêm tài xế mới (với mã tài xế)."""
            db = None
            try:
                db = Database()
                query = """
                    INSERT INTO TaiXe 
                    (ma_tai_xe, ho_ten, email, so_dien_thoai, hang_xe_lai, so_bang_lai, trang_thai) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    data['driver_code'],  # <-- THÊM THAM SỐ NÀY
                    data['name'],
                    data['email'],
                    data['phone'],
                    data['vehicle_category'],
                    data['license'],
                    data['status']
                )
                db.execute_query(query, params)
                return True
            except mysql.connector.Error as err:
                print(f"Lỗi khi thêm tài xế: {err}")
                return False
            finally:
                if db:
                    db.close()

    def update_driver(self, driver_code, data):
        """
        Cập nhật thông tin tài xế dựa trên ma_tai_xe.
        """
        db = None
        try:
            db = Database()

            query = """
                UPDATE `TaiXe` 
                SET `ho_ten` = %s, `email` = %s, `so_dien_thoai` = %s, 
                    `hang_xe_lai` = %s, `so_bang_lai` = %s, `trang_thai` = %s
                WHERE `ma_tai_xe` = %s
            """
            params = (
                data['name'],
                data['email'],
                data['phone'],
                data['vehicle_category'],
                data['license'],
                data['status'],
                driver_code
            )

            db.execute_query(query, params)
            return True

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Cập Nhật", f"Không thể cập nhật Tài xế:\n{err}")
            return False
        finally:
            if db:
                db.close()

    def delete_driver(self, driver_code):
        """
        Xóa tài xế khỏi CSDL dựa trên ma_tai_xe.
        """
        db = None
        try:
            db = Database()

            query = "DELETE FROM `TaiXe` WHERE `ma_tai_xe` = %s"
            params = (driver_code,)

            db.execute_query(query, params)
            return True

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Xóa", f"Không thể xóa Tài xế:\n{err}")
            return False
        finally:
            if db:
                db.close()