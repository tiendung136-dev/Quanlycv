import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date, datetime

# 1. Cấu hình trang
st.set_page_config(page_title="68ICC - Quản lý đồng bộ", layout="wide")

st.markdown("""
    <style>
    * { font-family: 'Times New Roman', Times, serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. Kết nối với Google Sheets
# DÁN LINK GOOGLE SHEETS CỦA ANH VÀO ĐÂY
url = "https://docs.google.com/spreadsheets/d/1lab3iWTMXu3fUihalIaQa-wPxA3EJW1H7rFs9b-rZXM/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

# Đọc dữ liệu mới nhất (ttl=0 để không bị trễ dữ liệu)
try:
    df = conn.read(spreadsheet=url, ttl=0)
except:
    # Nếu Sheets trống, tạo khung dữ liệu tạm thời
    df = pd.DataFrame(columns=["Dự án", "Hạng mục", "Trạng thái", "Bắt đầu", "Hạn"])

st.title("📋 HỆ THỐNG ĐỒNG BỘ PC & MOBILE - 68ICC")

# 3. Form nhập liệu
with st.expander("➕ THÊM CÔNG VIỆC MỚI"):
    with st.form("form_nhap", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1: ten = st.text_input("Tên dự án")
        with c2: hm = st.selectbox("Hạng mục", ["Cầu", "Đường", "Hạ tầng", "Khác"])
        with c3: tt = st.selectbox("Trạng thái", ["Đang thiết kế", "Chờ duyệt", "Hoàn thành"])
        
        c4, c5 = st.columns(2)
        with c4: n_bd = st.date_input("Ngày bắt đầu", value=date.today())
        with c5: n_h = st.date_input("Hạn hoàn thành", value=date.today())
        
        if st.form_submit_button("LƯU VÀ ĐỒNG BỘ"):
            if ten:
                # Tạo dòng mới
                new_data = pd.DataFrame([{
                    "Dự án": ten, "Hạng mục": hm, "Trạng thái": tt, 
                    "Bắt đầu": n_bd.strftime('%Y-%m-%d'), 
                    "Hạn": n_h.strftime('%Y-%m-%d')
                }])
                # Ghép vào dữ liệu cũ
                updated_df = pd.concat([df, new_data], ignore_index=True)
                # Đẩy ngược lên Google Sheets
                conn.update(spreadsheet=url, data=updated_df)
                st.success("Đã đồng bộ dữ liệu!")
                st.rerun()

# 4. Hiển thị danh sách & Cảnh báo màu
st.subheader("📊 DANH MỤC CÔNG VIỆC HIỆN TẠI")

if not df.empty:
    # Chuyển định dạng ngày để tô màu
    df['Hạn'] = pd.to_datetime(df['Hạn']).dt.date
    
    def highlight_rows(row):
        days_left = (row['Hạn'] - date.today()).days
        if days_left < 0: return ['background-color: #ff4b4b; color: white'] * len(row)
        if 0 <= days_left <= 3: return ['background-color: #ffa500; color: black'] * len(row)
        return [''] * len(row)

    st.dataframe(df.style.apply(highlight_rows, axis=1), use_container_width=True)
    
    # Nút Xóa dòng
    st.markdown("---")
    idx_del = st.number_input("STT dòng cần xóa (từ 0):", min_value=0, max_value=len(df)-1, step=1)
    if st.button("🗑️ XÓA DÒNG NÀY"):
        df = df.drop(df.index[idx_del])
        conn.update(spreadsheet=url, data=df)
        st.warning("Đã xóa và cập nhật hệ thống!")
        st.rerun()
else:
    st.info("Chưa có dữ liệu. Anh hãy nhập dự án đầu tiên nhé!")
