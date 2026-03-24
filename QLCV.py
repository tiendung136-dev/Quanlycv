import streamlit as st
import pandas as pd
from datetime import datetime, date

# 1. Cấu hình trang giao diện khổ ngang (A3)
st.set_page_config(page_title="68ICC - Quản lý công việc", layout="wide")

# Áp dụng font Times New Roman
st.markdown("""
    <style>
    * { font-family: 'Times New Roman', Times, serif; }
    .stApp { background-color: #f4f7f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. Khởi tạo bộ nhớ tạm (Giúp lưu dữ liệu khi bấm nút)
if 'danh_sach_viec' not in st.session_state:
    # Dữ liệu mẫu ban đầu
    st.session_state.danh_sach_viec = [
        {"Dự án": "Cầu vượt nút giao 72m", "Hạng mục": "Cầu", "Trạng thái": "Đang thiết kế", "Bắt đầu": date(2026, 3, 10), "Hạn": date(2026, 3, 20)},
        {"Dự án": "Nâng cấp QL1A Vinh", "Hạng mục": "Đường", "Trạng thái": "Chờ duyệt", "Bắt đầu": date(2026, 3, 1), "Hạn": date(2026, 3, 28)}
    ]

st.title("📋 HỆ THỐNG QUẢN LÝ DỰ ÁN 68ICC")

# 3. Khu vực nhập liệu (Form)
with st.expander("➕ THÊM CÔNG VIỆC MỚI", expanded=True):
    with st.form("form_nhap_lieu", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            ten_du_an = st.text_input("Tên dự án/Gói thầu")
        with col2:
            hang_muc = st.selectbox("Hạng mục", ["Cầu", "Đường", "Hạ tầng", "Khác"])
        with col3:
            trang_thai = st.selectbox("Trạng thái", ["Đang thiết kế", "Chờ duyệt", "Hoàn thành"])
        
        col4, col5 = st.columns(2)
        with col4:
            ngay_bd = st.date_input("Ngày bắt đầu", value=date.today())
        with col5:
            ngay_han = st.date_input("Hạn hoàn thành", value=date.today())
        
        submit = st.form_submit_button("LƯU DỰ ÁN")
        
        if submit:
            if ten_du_an:
                new_task = {
                    "Dự án": ten_du_an,
                    "Hạng mục": hang_muc,
                    "Trạng thái": trang_thai,
                    "Bắt đầu": ngay_bd,
                    "Hạn": ngay_han
                }
                st.session_state.danh_sach_viec.append(new_task)
                st.success(f"Đã thêm: {ten_du_an}")
                st.rerun()
            else:
                st.error("Vui lòng nhập tên dự án!")

# 4. Hiển thị Danh mục & Cảnh báo màu
st.subheader("📊 DANH MỤC CÔNG VIỆC ĐANG THỰC HIỆN")

if st.session_state.danh_sach_viec:
    df = pd.DataFrame(st.session_state.danh_sach_viec)
    
    # Hàm tô màu logic
    def highlight_rows(row):
        today = date.today()
        # Tính khoảng cách ngày
        days_left = (row['Hạn'] - today).days
        
        if days_left < 0:
            return ['background-color: #ff4b4b; color: white'] * len(row) # Đỏ: Quá hạn
        elif 0 <= days_left <= 3:
            return ['background-color: #ffa500; color: black'] * len(row) # Cam: Sắp hạn
        return [''] * len(row)

    # Hiển thị bảng xịn xò
    st.dataframe(
        df.style.apply(highlight_rows, axis=1),
        use_container_width=True,
        height=500
    )
else:
    st.info("Chưa có công việc nào trong danh sách.")

st.markdown("---")
st.caption("Thiết kế bởi 68ICC - Hỗ trợ hiển thị tốt nhất trên máy tính và điện thoại xoay ngang.")
