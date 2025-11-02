import mysql.connector
import os
from dotenv import load_dotenv
from os.path import join, dirname

# Tìm file .env ở thư mục gốc (cao hơn 2 cấp so với file này)
dotenv_path = join(dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

def get_db_connection():
    """
    Tạo và trả về một kết nối đến CSDL MySQL.
    Sử dụng các biến môi trường từ file .env.
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('3306'),
            user=os.getenv('root'),
            password=os.getenv('11022005'),
            database=os.getenv('QLXEVALAIXE')
        )
        if conn.is_connected():
            return conn
    except mysql.connector.Error as err:
        print(f"[LỖI KẾT NỐI DB]: {err}")
        return None
    except Exception as e:
        print(f"[LỖI CHUNG]: {e}")
        return None
