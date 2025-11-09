from .db_connect import Database
import mysql.connector


class VehicleModel:

    def get_all_vehicles(self, status=None):
        """
        Lấy tất cả phương tiện từ CSDL, có thể lọc theo trạng thái.
        Sử dụng JOIN để lấy tên tài xế thay vì mã.
        """
        db = None
        try:
            db = Database()

            # Câu query này sử dụng LEFT JOIN để lấy `ho_ten` từ bảng `TaiXe`
            # COALESCE dùng để hiển thị '(Chưa gán)' nếu `ma_tai_xe_phu_trach` là NULL
            query = """
                SELECT 
                    v.bien_so_xe, 
                    v.loai_xe, 
                    COALESCE(t.ho_ten, '(Chưa gán)'), 
                    v.so_km_da_di, 
                    v.ngay_bao_tri_cuoi, 
                    v.trang_thai 
                FROM PhuongTien AS v
                LEFT JOIN TaiXe AS t 
                    ON v.ma_tai_xe_phu_trach = t.ma_tai_xe
            """

            params = []
            if status:
                query += " WHERE v.trang_thai = %s"
                params.append(status)

            # fetch_all không cần params nếu params rỗng
            if params:
                return db.fetch_all(query, params)
            else:
                return db.fetch_all(query)

        except mysql.connector.Error as err:
            print(f"Lỗi khi lấy dữ liệu Phương tiện: {err}")
            return []
        finally:
            if db:
                db.close()

    # (Bạn có thể thêm các hàm add_vehicle, update_vehicle, delete_vehicle ở đây)