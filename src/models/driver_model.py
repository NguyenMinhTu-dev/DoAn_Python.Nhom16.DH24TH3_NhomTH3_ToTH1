from .db_connect import Database
import mysql.connector


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

            # fetch_all không cần params nếu params rỗng
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

    # (Bạn có thể thêm các hàm add_driver, update_driver, delete_driver ở đây)