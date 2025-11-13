from .db_connect import Database
import mysql.connector
from tkinter import messagebox


class VehicleModel:

    def get_all_vehicles(self, status=None):
        """Lấy tất cả phương tiện từ CSDL, có thể lọc theo trạng thái."""
        db = None
        try:
            db = Database()
            query = """
                SELECT 
                    id_phuong_tien,
                    bien_so_xe,
                    loai_xe,
                    so_km_da_di,
                    ngay_bao_tri_cuoi,
                    trang_thai,
                    ma_tai_xe_phu_trach
                FROM PhuongTien
            """
            params = []
            if status:
                query += " WHERE trang_thai = %s"
                params.append(status)

            return db.fetch_all(query, params) if params else db.fetch_all(query)

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi DB", f"Lỗi khi tải dữ liệu Phương tiện: {err}")
            return []
        finally:
            if db:
                db.close()

    def get_all_drivers(self, status=None):
        """Lấy tất cả tài xế để cho Combobox chọn."""
        db = None
        try:
            db = Database()
            query = "SELECT ma_tai_xe, ho_ten FROM TaiXe"
            params = []
            if status:
                query += " WHERE trang_thai = %s"
                params.append(status)
            return db.fetch_all(query, params) if params else db.fetch_all(query)
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi DB", f"Lỗi khi tải danh sách tài xế: {err}")
            return []
        finally:
            if db:
                db.close()

    def add_vehicle(self, data):
        """Thêm một phương tiện mới, cho phép driver_code rỗng (để tránh lỗi FK)."""
        db = None
        try:
            db = Database()
            driver_code = data.get('driver_code', None) or None  # Nếu rỗng => None

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
                driver_code
            )

            db.execute_query(query, params)
            return True

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Thêm Mới", f"Không thể thêm Phương tiện:\n{err}")
            return False
        finally:
            if db:
                db.close()

    def update_vehicle(self, plate, data):
        """Cập nhật thông tin phương tiện, driver_code có thể None."""
        db = None
        try:
            db = Database()
            driver_code = data.get('driver_code', None) or None

            query = """
                UPDATE PhuongTien
                SET loai_xe = %s,
                    so_km_da_di = %s,
                    ngay_bao_tri_cuoi = %s,
                    trang_thai = %s,
                    ma_tai_xe_phu_trach = %s
                WHERE bien_so_xe = %s
            """
            params = (
                data['type'],
                data['mileage'],
                data['last_maintenance'],
                data['status'],
                driver_code,
                plate
            )

            db.execute_query(query, params)
            return True

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Cập Nhật", f"Không thể cập nhật Phương tiện:\n{err}")
            return False
        finally:
            if db:
                db.close()

    def delete_vehicle(self, plate):
        """Xóa phương tiện khỏi CSDL dựa trên biển số."""
        db = None
        try:
            db = Database()
            query = "DELETE FROM PhuongTien WHERE bien_so_xe = %s"
            params = (plate,)
            db.execute_query(query, params)
            return True

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Xóa", f"Không thể xóa Phương tiện:\n{err}")
            return False
        finally:
            if db:
                db.close()

    def edit_vehicle(self, vehicle_id, data):
        """
        Cập nhật thông tin phương tiện dựa trên id_phuong_tien.
        data: dict chứa thông tin mới (type, mileage, last_maintenance, status, driver_code)
        driver_code có thể None nếu không muốn gán tài xế
        """
        db = None
        try:
            db = Database()
            driver_code = data.get('driver_code', None) or None  # None nếu rỗng

            query = """
                UPDATE PhuongTien
                SET loai_xe = %s,
                    so_km_da_di = %s,
                    ngay_bao_tri_cuoi = %s,
                    trang_thai = %s,
                    ma_tai_xe_phu_trach = %s
                WHERE id_phuong_tien = %s
            """
            params = (
                data['type'],
                data['mileage'],
                data['last_maintenance'],
                data['status'],
                driver_code,
                vehicle_id
            )

            db.execute_query(query, params)
            return True

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Cập Nhật", f"Không thể cập nhật phương tiện:\n{err}")
            return False
        finally:
            if db:
                db.close()
