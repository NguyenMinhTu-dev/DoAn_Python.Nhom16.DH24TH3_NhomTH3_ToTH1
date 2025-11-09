from .db_connect import Database
import mysql.connector


class CustomerModel:

    def get_all_customers(self, rank=None):
        """
        Lấy tất cả khách hàng từ CSDL, có thể lọc theo hạng thành viên.
        """
        db = None
        try:
            db = Database()

            # Câu query này chọn các cột khớp với Treeview
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
            if rank:
                query += " WHERE hang_thanh_vien = %s"
                params.append(rank)

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

    # (Bạn có thể thêm các hàm add_customer, update_customer, delete_customer ở đây)