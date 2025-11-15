from .db_connect import Database
import mysql.connector


class CustomerModel:

    # (Đây là code để bạn chép vào file models/customer_model.py)

    def get_all_customers(self, rank=None, search=None):
        """
        Lấy tất cả khách hàng, có thể lọc theo HẠNG và TÌM KIẾM.
        """
        db = None
        try:
            db = Database()
            query = """
                    SELECT 
                        id_khach_hang, 
                        ho_ten, 
                        so_dien_thoai, 
                        email,  
                        hang_thanh_vien 
                    FROM KhachHang
                """

            params = []
            conditions = []  # Dùng để nối các điều kiện WHERE

            # 1. Xử lý lọc theo Hạng (rank)
            if rank:
                conditions.append("hang_thanh_vien = %s")
                params.append(rank)

            # 2. Xử lý lọc theo Tìm kiếm (search)
            if search:
                # Tìm kiếm ở 3 cột: Mã, Tên, SĐT
                search_like = f"%{search}%"
                conditions.append("""
                        (id_khach_hang LIKE %s OR 
                         ho_ten LIKE %s OR 
                         so_dien_thoai LIKE %s)
                    """)
                params.extend([search_like, search_like, search_like])

            # 3. Nối các điều kiện lại
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY id_khach_hang"

            if params:
                return db.fetch_all(query, params)
            else:
                return db.fetch_all(query)

        except mysql.connector.Error as err:
            print(f"Lỗi khi lấy dữ liệu Khách hàng: {err}")
            return []
        finally:
            if db:
                db.close()

    # === HÀM MỚI CHO MODAL ===

    def add_customer(self, data):
        """
        Thêm một khách hàng mới vào CSDL.
        'data' là một dictionary chứa: 'name', 'email', 'phone', 'rank'.
        """
        db = None
        try:
            db = Database()

            # Lưu ý: Bỏ qua id_khach_hang (vì nó tự động tăng hoặc được trigger)
            query = """
                INSERT INTO KhachHang 
                    (ho_ten, email, so_dien_thoai, hang_thanh_vien) 
                VALUES 
                    (%s, %s, %s, %s)
            """
            params = (
                data.get('name'),
                data.get('email'),
                data.get('phone'),
                data.get('rank')
            )

            db.execute_query(query, params)
            return True  # Trả về True nếu thành công

        except mysql.connector.Error as err:
            print(f"Lỗi khi thêm khách hàng: {err}")
            return False  # Trả về False nếu thất bại
        finally:
            if db:
                db.close()

    # === HÀM MỚI CHO MODAL ===

    def update_customer(self, customer_code, data):
        """
        Cập nhật thông tin khách hàng dựa trên ID.
        'customer_code' là ID (vd: 'KH001').
        'data' là một dictionary chứa: 'name', 'email', 'phone', 'rank'.
        """
        db = None
        try:
            db = Database()
            query = """
                UPDATE KhachHang SET
                    ho_ten = %s,
                    email = %s,
                    so_dien_thoai = %s,
                    hang_thanh_vien = %s
                WHERE 
                    id_khach_hang = %s
            """
            params = (
                data.get('name'),
                data.get('email'),
                data.get('phone'),
                data.get('rank'),
                customer_code  # ID khách hàng cho mệnh đề WHERE
            )

            db.execute_query(query, params)
            return True

        except mysql.connector.Error as err:
            print(f"Lỗi khi cập nhật khách hàng {customer_code}: {err}")
            return False
        finally:
            if db:
                db.close()

    # === HÀM MỚI CHO NÚT XÓA ===

    def delete_customer(self, customer_code):
        """
        Xóa một khách hàng khỏi CSDL dựa trên ID.
        """
        db = None
        try:
            db = Database()

            # Cẩn thận: Đảm bảo CSDL cho phép xóa
            # (Ví dụ: nếu khách hàng đã có chuyến đi, có thể sẽ lỗi
            # do ràng buộc khóa ngoại - Foreign Key Constraint)

            query = "DELETE FROM KhachHang WHERE id_khach_hang = %s"
            params = (customer_code,)

            db.execute_query(query, params)
            return True

        except mysql.connector.Error as err:
            # Lỗi thường gặp: Lỗi ràng buộc khóa ngoại
            if err.errno == 1451:  # Foreign key constraint fails
                print(f"Lỗi 1451: Không thể xóa khách hàng {customer_code} vì họ có dữ liệu liên quan (chuyến xe).")
            else:
                print(f"Lỗi khi xóa khách hàng {customer_code}: {err}")
            return False
        finally:
            if db:
                db.close()

        # (Các hàm get_all_customers, add_customer, v.v. đã có ở trên)

    def get_customer_stats(self):
            """
            Lấy số liệu thống kê cho 3 thẻ trên trang Quản lý Khách Hàng.
            """
            db = None
            try:
                db = Database()

                # 1. Đếm tổng số khách hàng
                query_total = "SELECT COUNT(*) FROM KhachHang"
                total_count = db.fetch_one(query_total)[0]

                # 2. Đếm khách VIP
                query_vip = "SELECT COUNT(*) FROM KhachHang WHERE hang_thanh_vien = 'VIP'"
                vip_count = db.fetch_one(query_vip)[0]

                # 3. Đếm khách Bạc
                query_silver = "SELECT COUNT(*) FROM KhachHang WHERE hang_thanh_vien = 'Bạc'"
                silver_count = db.fetch_one(query_silver)[0]

                # Trả về một dictionary
                return {
                    "total": total_count or 0,
                    "vip": vip_count or 0,
                    "silver": silver_count or 0
                }

            except mysql.connector.Error as err:
                print(f"Lỗi khi lấy số liệu thống kê khách hàng: {err}")
                return {"total": 0, "vip": 0, "silver": 0}
            finally:
                if db:
                    db.close()