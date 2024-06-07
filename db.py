import sqlite3

def init_db():
    conn = sqlite3.connect("movie.sqlite")
    cursor = conn.cursor()

    # Kiểm tra sự tồn tại của bảng
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movie'")
    table_exists = cursor.fetchone()

    # Nếu bảng không tồn tại, tạo bảng mới
    if not table_exists:
        sql_query = """
        CREATE TABLE movie (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL,
            director TEXT NOT NULL,
            poster TEXT,
            trailer TEXT
        )
        """
        cursor.execute(sql_query)
        conn.commit()

    conn.close()
