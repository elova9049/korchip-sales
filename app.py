# app.py
import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# DB 연결
conn = sqlite3.connect("supercap.db")

# 로그인 페이지
if "user" not in st.session_state:
    st.title("🔒 슈퍼캡 관리 시스템 로그인")
    
    username = st.text_input("아이디")
    password = st.text_input("패스워드", type="password")
    
    if st.button("로그인"):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()
        
        if user:
            st.session_state["user"] = {
                "id": user[0],
                "name": user[1],
                "role": user[3],
                "customers": user[4].split(",") if user[4] != "ALL" else "ALL"
            }
            st.rerun()
        else:
            st.error("😢 아이디 또는 비밀번호가 틀렸습니다.")

# 로그인 후 대시보드
else:
    user = st.session_state["user"]
    st.title(f"👋 {user['name']}님, 환영합니다!")
    
    # 제조지시서 입력 폼
    with st.form("order_form"):
        st.subheader("📝 새 제조지시서 작성")
        customer = st.selectbox(
            "고객사",
            ["고객사A", "고객사B", "고객사C"] if user["customers"] == "ALL" else user["customers"]
        )
        product = st.text_input("품목코드 (예: CAP-001)")
        qty = st.number_input("수량", min_value=1, value=100)
        prod_days = st.slider("제조 소요일수", 1, 10, 3)
        
        if st.form_submit_button("저장"):
            due_date = (datetime.now() + timedelta(days=prod_days)).strftime("%Y-%m-%d")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO manufacturing_orders VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",
                (customer, product, qty, prod_days, datetime.now().strftime("%Y-%m-%d"), 
                 due_date, "진행중", user["name"])
            )
            conn.commit()
            st.success(f"✅ 저장 완료! 납기예정일: {due_date}")
    
    # 주문 현황 표시
    st.divider()
    st.subheader("📊 나의 주문 현황")
    
    query = "SELECT * FROM manufacturing_orders" if user["role"] == "admin" else \
            f"SELECT * FROM manufacturing_orders WHERE assigned_to='{user['name']}'"
    
    orders = conn.cursor().execute(query).fetchall()
    if orders:
        st.table(orders)
    else:
        st.info("📭 표시할 주문이 없습니다.")
