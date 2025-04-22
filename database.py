# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect("supercap.db")
    cursor = conn.cursor()

    # 사용자 테이블
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        assigned_customers TEXT
    )
    """)

    # 주문 테이블
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manufacturing_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        product_code TEXT,
        quantity INTEGER,
        production_days INTEGER,
        order_date TEXT,
        due_date TEXT,
        status TEXT,
        assigned_to TEXT
    )
    """)

    # 테스트 데이터
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', '1234', 'admin', 'ALL')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, '직원1', '1234', 'employee', '고객사A,고객사B')")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized!")
