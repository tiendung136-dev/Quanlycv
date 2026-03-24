import streamlit as st
import pandas as pd
from datetime import date

# Cấu hình trang để hiển thị đẹp trên điện thoại
st.set_page_config(page_title="68ICC Manager", layout="centered")

st.title("📱 Quản lý Công việc 68ICC")

# Tạo các Tab để chuyển đổi nhanh trên điện thoại
tab1, tab2 = st.tabs(["➕ Thêm việc", "📊 Danh sách"])

with tab1:
    st.subheader("Nhập thông tin dự án")
    with st.form("my_form", clear_on_submit=True):
        project = st.text_input("Tên nút giao/Dự án")
        task = st.text_input("Hạng mục chi tiết")
        deadline = st.date_input("Hạn định", date.today())
        status = st.selectbox("Trạng thái", ["Đang làm", "Chờ duyệt", "Xong"])
        
        submitted = st.form_submit_button("LƯU DỮ LIỆU")
        if submitted:
            # Code lưu vào file Excel/CSV ở đây
            st.success("Đã ghi nhận công việc!")

with tab2:
    st.subheader("Tiến độ hiện tại")
    # Giả sử đọc dữ liệu từ file
    data = {"Dự án": ["Nút giao QL1", "Đường 72m"], "Trạng thái": ["Đang làm", "Xong"]}
    df = pd.DataFrame(data)
    st.table(df) # Dùng table sẽ dễ nhìn hơn dataframe trên màn hình nhỏ