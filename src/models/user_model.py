from  src.database.database_connector import get_db_connection
import bcrypt


def verify_login(email_or_phone, password_goc):
    """
    Kiểm tra thông tin đăng nhập với CSDL.
    Trả về (vai_tro, id_tai_khoan) nếu thành công, ngược lại trả về None.
    """
    conn = get_db_connection()
    if not conn:
        print("[LỖI]: Không thể kết nối CSDL để xác minh.")
        return None

    cursor = conn.cursor(dictionary=True)  # dictionary=True để lấy kết quả dạng {tên_cột: giá_trị}

    try:
        # Truy vấn CSDL
        query = """
        SELECT id_tai_khoan, mat_khau_hash, vai_tro 
        FROM TaiKhoan 
        WHERE email = %s OR so_dien_thoai = %s
        """
        cursor.execute(query, (email_or_phone, email_or_phone))
        account = cursor.fetchone()

        if not account:
            print("[XÁC MINH]: Không tìm thấy tài khoản.")
            return None  # Không tìm thấy tài khoản

        # Lấy hash từ CSDL
        mat_khau_hash_tu_db = account['mat_khau_hash'].encode('utf-8')
        password_goc_bytes = password_goc.encode('utf-8')

        # Kiểm tra mật khẩu
        if bcrypt.checkpw(password_goc_bytes, mat_khau_hash_tu_db):
            # Mật khẩu khớp
            print("[XÁC MINH]: Đăng nhập thành công.")
            return (account['vai_tro'], account['id_tai_khoan'])
        else:
            # Mật khẩu sai
            print("[XÁC MINH]: Mật khẩu không đúng.")
            return None

    except Exception as e:
        print(f"[LỖI XÁC MINH LOGIN]: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# --- CÁC HÀM QUẢN LÝ TÀI KHOẢN (CRUD) ---
# (Các model khác sẽ gọi các hàm này)

def create_account(cursor, ho_ten, email, so_dien_thoai, password_goc, vai_tro):
    """Tạo tài khoản mới và trả về ID. Cần truyền cursor để dùng trong transaction."""
    try:
        salt = bcrypt.gensalt()
        mat_khau_hash = bcrypt.hashpw(password_goc.encode('utf-8'), salt)

        query = """
        INSERT INTO TaiKhoan (ho_ten, email, so_dien_thoai, mat_khau_hash, vai_tro, ngay_tao) 
        VALUES (%s, %s, %s, %s, %s, CURDATE())
        """
        cursor.execute(query, (ho_ten, email, so_dien_thoai, mat_khau_hash.decode('utf-8'), vai_tro))
        return cursor.lastrowid  # Trả về ID của tài khoản vừa tạo
    except Exception as e:
        print(f"[LỖI CREATE_ACCOUNT]: {e}")
        raise  # Ném lỗi ra ngoài để transaction có thể rollback


def delete_account(cursor, id_tai_khoan):
    """Xóa tài khoản. Cần truyền cursor."""
    try:
        query = "DELETE FROM TaiKhoan WHERE id_tai_khoan = %s"
        cursor.execute(query, (id_tai_khoan,))
        return True
    except Exception as e:
        print(f"[LỖI DELETE_ACCOUNT]: {e}")
        raise

