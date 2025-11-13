from .db_connect import Database
import mysql.connector
from tkinter import messagebox


class VehicleModel:

    def get_all_vehicles(self, status=None):
        """
        Lấy tất cả phương tiện từ CSDL, có thể lọc theo trạng thái.
        """
        db = None
        try:
            db = Database()

            query = """
                SELECT 
                    `id_phuong_tien`,
                    `bien_so_xe`,
                    `loai_xe`,
                    `so_km_da_di`,
                    `ngay_bao_tri_cuoi`,
                    `trang_thai`,
                    `ma_tai_xe_phu_trach`
                FROM `PhuongTien`
            """
            params = []
            if status:
                query += " WHERE `trang_thai` = %s"
                params.append(status)

            # Sử dụng params nếu có, nếu không thì gọi query không tham số
            return db.fetch_all(query, params) if params else db.fetch_all(query)

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi DB", f"Lỗi khi tải dữ liệu Phương tiện: {err}")
            return []
        finally:
            if db:
                db.close()

    def add_vehicle(self, data):
        """
        Thêm một phương tiện mới vào CSDL.
        Đã thêm db.conn.commit() và xử lý chuỗi rỗng cho mã tài xế.
        """
        db = None
        try:
            db = Database()

            # Chuyển chuỗi rỗng thành None để INSERT NULL vào DB nếu cột cho phép
            driver_code = data.get('driver_code')
            if driver_code == '':
                driver_code = None

            query = """
                INSERT INTO `PhuongTien` 
                (`bien_so_xe`, `loai_xe`, `so_km_da_di`, `ngay_bao_tri_cuoi`, `trang_thai`, `ma_tai_xe_phu_trach`)
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
            db.conn.commit()  # <<< Đảm bảo thay đổi được lưu
            return True

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Thêm Mới", f"Không thể thêm Phương tiện:\n{err}")
            return False
        finally:
            if db:
                db.close()

    def update_vehicle_by_id(self, vehicle_id, data):
        """
        Cập nhật thông tin phương tiện dựa trên id_phuong_tien.
        Đã xử lý chuỗi rỗng cho mã tài xế và đảm bảo commit.
        """
        db = None
        try:
            db = Database()

            # Chuyển chuỗi rỗng thành None
            driver_code = data.get('driver_code')
            if driver_code == '':
                driver_code = None

            query = """
                UPDATE PhuongTien
                SET bien_so_xe=%s, loai_xe=%s, so_km_da_di=%s,
                    ngay_bao_tri_cuoi=%s, trang_thai=%s, ma_tai_xe_phu_trach=%s
                WHERE id_phuong_tien=%s
            """
            params = (
                data['plate'],
                data['type'],
                data['mileage'],
                data['last_maintenance'],
                data['status'],
                driver_code,
                vehicle_id
            )

            db.execute_query(query, params)
            db.conn.commit()  # <<< Đảm bảo thay đổi được lưu
            return True

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Cập Nhật", f"Không thể cập nhật Phương tiện:\n{err}")
            return False
        finally:
            if db:
                db.close()

    def delete_vehicle(self, plate):
        """
        Xóa phương tiện dựa trên biển số xe.
        """
        db = None
        try:
            db = Database()
            query = "DELETE FROM PhuongTien WHERE bien_so_xe = %s"
            params = (plate,)
            db.execute_query(query, params)
            db.conn.commit()  # Commit để thay đổi lưu lại
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Xóa", f"Không thể xóa Phương tiện:\n{err}")
            return False
        finally:
            if db:
                db.close()

    def get_all_drivers(self, status=None):
        """
        Lấy tất cả tài xế để hiển thị trong Combobox, có thể lọc theo trạng thái.
        """
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

    def get_vehicle_by_id(self, vehicle_id):
        """
        Lấy thông tin chi tiết của phương tiện theo ID.
        """
        db = None
        try:
            db = Database()
            query = """
                SELECT id_phuong_tien, bien_so_xe, loai_xe, so_km_da_di, 
                       ngay_bao_tri_cuoi, trang_thai, ma_tai_xe_phu_trach
                FROM PhuongTien
                WHERE id_phuong_tien = %s
            """
            result = db.fetch_one(query, (vehicle_id,))
            if result:
                return {
                    'id_phuong_tien': result[0],
                    'bien_so_xe': result[1],
                    'loai_xe': result[2],
                    'so_km_da_di': result[3],
                    'ngay_bao_tri_cuoi': result[4],
                    'trang_thai': result[5],
                    'ma_tai_xe_phu_trach': result[6]
                }
            return None
        finally:
            if db:
                db.close()

    def is_plate_exists(self, plate, exclude_vehicle_id=None):
        """
        Kiểm tra xem biển số xe đã tồn tại trong DB chưa, loại trừ chính xe đang sửa.
        """
        db = None
        try:
            db = Database()
            query = "SELECT COUNT(*) FROM PhuongTien WHERE bien_so_xe=%s"
            params = [plate]
            if exclude_vehicle_id:
                query += " AND id_phuong_tien <> %s"
                params.append(exclude_vehicle_id)

            result = db.fetch_one(query, params)
            return result[0] > 0 if result else False

        except Exception as e:
            print(f"Lỗi kiểm tra biển số: {e}")
            return False
        finally:
            if db:
                db.close()