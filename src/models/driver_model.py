from .db_connect import Database
import mysql.connector
from tkinter import messagebox  # Cần để hiển thị lỗi DB


class DriverModel:

    def get_all_drivers(self, status=None):
        """
        Lấy tất cả tài xế từ CSDL, có thể lọc theo trạng thái.
        """
        db = None
        try:
            db = Database()

            # Câu query này phải khớp với CSDL tiếng Việt của bạn
            query = """
                SELECT 
                    `ma_tai_xe`, 
                    `ho_ten`, 
                    `hang_xe_lai`, 
                    `so_bang_lai`, 
                    `email`, 
                    `so_dien_thoai`, 
                    `danh_gia_trung_binh`, 
                    `trang_thai` 
                FROM `TaiXe`
            """

            params = []
            if status:
                query += " WHERE `trang_thai` = %s"
                params.append(status)

            if params:
                return db.fetch_all(query, params)
            else:
                return db.fetch_all(query)

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi DB", f"Lỗi khi tải dữ liệu Tài xế: {err}")
            return []
        finally:
            if db:
                db.close()

    def add_driver(self, data):
        """
        Thêm một tài xế mới vào CSDL.
        data là một dictionary chứa thông tin tài xế.
        """
        db = None
        try:
            db = Database()

            # Tạm thời bỏ qua `ma_tai_xe` vì CSDL không có auto-increment cho cột này.
            # CSDL cần phải có logic tạo mã (hoặc bạn tự tạo mã TX00X).

            query = """
                INSERT INTO `TaiXe` 
                (`ho_ten`, `email`, `so_dien_thoai`, `hang_xe_lai`, `so_bang_lai`, `trang_thai`)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
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
            messagebox.showerror("Lỗi Thêm Mới", f"Không thể thêm Tài xế:\n{err}")
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