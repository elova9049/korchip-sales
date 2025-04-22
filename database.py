import sqlite3

def init_db():
    try:
        conn = sqlite3.connect("supercap.db", check_same_thread=False)
        cursor = conn.cursor()

        # 사용자 테이블
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            assigned_customers TEXT  # 오타 수정: assigned_customers (원래는 assigned_customers)
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
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db()
