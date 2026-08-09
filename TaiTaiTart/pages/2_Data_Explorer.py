"""
Data Explorer Page - Egg Tart Sales Dashboard
Pages File: pages/2_Data_Explorer.py
Developer: OriZaMa Channel
"""

import streamlit as st
import pandas as pd
from utils.components import inject_custom_css, render_header, render_footer
from utils.data_utils import load_sample_data, load_uploaded_data, clean_data, filter_data

st.set_page_config(
    page_title="Data Explorer | ระบบวิเคราะห์ยอดขายร้านขายทาร์ตไข่",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

render_header(
    title="📋 Data Explorer (สำรวจและจัดการข้อมูล)",
    subtitle="ตรวจสอบข้อมูลดิบ, ข้อมูลที่ผ่านการทำความสะอาด, ค้นหา, กรอง และส่งออกรายงาน CSV",
    icon="📋"
)

# -------------------------------------------------------------
# 1. Sidebar - Data Source
# -------------------------------------------------------------
st.sidebar.markdown("## ⚙️ แหล่งข้อมูล")

data_source = st.sidebar.radio(
    "📁 เลือกแหล่งข้อมูล (Data Source):",
    options=["ใช้ข้อมูลตัวอย่าง (Sample Data)", "อัปโหลดไฟล์ (Upload CSV / Excel)"],
    index=0
)

df_raw = None

if data_source == "ใช้ข้อมูลตัวอย่าง (Sample Data)":
    df_raw = load_sample_data()
    st.sidebar.success("✅ โหลดข้อมูลตัวอย่างสำเร็จ (320 รายการ)")
else:
    uploaded_file = st.sidebar.file_uploader(
        "อัปโหลดไฟล์ .csv หรือ .xlsx",
        type=["csv", "xlsx"]
    )
    if uploaded_file is not None:
        df_raw, err_msg = load_uploaded_data(uploaded_file)
        if err_msg:
            st.error(f"❌ {err_msg}")
            st.stop()
        else:
            st.sidebar.success("✅ อัปโหลดและโหลดข้อมูลสำเร็จ!")
    else:
        st.info("ℹ️ กรุณาอัปโหลดไฟล์ CSV หรือ Excel ทาง Sidebar ซ้ายมือเพื่อเริ่มใช้งาน")
        st.stop()

# Data Cleaning
df_clean = clean_data(df_raw)

# -------------------------------------------------------------
# 2. Main Data Exploration Views (Tabs for Raw, Cleaned, Filtered Data)
# -------------------------------------------------------------
st.markdown("### 🗂️ เลือกมุมมองข้อมูล (Data Views)")

tab_filtered, tab_clean, tab_raw = st.tabs([
    "🔍 1. ข้อมูลหลังใช้ตัวกรอง (Filtered Data)",
    "🧹 2. ข้อมูลหลังทำความสะอาด (Cleaned Data)",
    "📄 3. ข้อมูลดิบ (Raw Data)"
])

# Determine active tab data
with tab_filtered:
    st.info("💡 **โหมดตัวกรอง:** ข้อมูลนี้จะถูกกรองตามเงื่อนไขทาง Sidebar ซ้ายมือ")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 ตัวกรองข้อมูล (Filtered Data Mode)")
    
    min_date = df_clean['order_date'].min().date()
    max_date = df_clean['order_date'].max().date()
    
    selected_dates = st.sidebar.date_input(
        "📅 ช่วงวันที่:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    branches = sorted(df_clean['branch'].unique().tolist())
    selected_branches = st.sidebar.multiselect("🏬 สาขา:", options=branches, default=branches)
    
    products = sorted(df_clean['product_name'].unique().tolist())
    selected_products = st.sidebar.multiselect("🥧 สินค้า:", options=products, default=products)
    
    payments = sorted(df_clean['payment_method'].unique().tolist())
    selected_payments = st.sidebar.multiselect("💳 วิธีชำระเงิน:", options=payments, default=payments)
    
    df_filtered_view = filter_data(
        df_clean,
        date_range=selected_dates if len(selected_dates) == 2 else None,
        selected_branches=selected_branches,
        selected_products=selected_products,
        selected_payments=selected_payments
    )

with tab_clean:
    st.info("🧹 **โหมดข้อมูลสะอาด:** ข้อมูลที่แปลงประเภทข้อมูล จัดการค่าสูญหาย และคำนวณ `net_sales` เรียบร้อยแล้ว")

with tab_raw:
    st.info("📄 **โหมดข้อมูลดิบ:** ข้อมูลดั้งเดิมที่อ่านจากไฟล์ก่อนการประมวลผลหรือทำความสะอาด")

# Select view mode dataframe based on user interaction
view_mode = st.radio(
    "โหมดแสดงผลในตารางขณะนี้:",
    options=["ข้อมูลที่กรองแล้ว (Filtered Data)", "ข้อมูลหลังทำความสะอาด (Cleaned Data)", "ข้อมูลดิบ (Raw Data)"],
    horizontal=True
)

if view_mode == "ข้อมูลดิบ (Raw Data)":
    df_display = df_raw.copy()
elif view_mode == "ข้อมูลหลังทำความสะอาด (Cleaned Data)":
    df_display = df_clean.copy()
else:
    df_display = df_filtered_view.copy()


# -------------------------------------------------------------
# 3. Search, Select Columns & Sorting Controls
# -------------------------------------------------------------
st.markdown("---")
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 1.5, 1])

with ctrl_col1:
    search_query = st.text_input("🔍 ค้นหาในตาราง (Search):", placeholder="พิมพ์รหัสออเดอร์, สาขา, ชื่อเมนู...")

with ctrl_col2:
    all_cols = list(df_display.columns)
    selected_cols = st.multiselect("📌 เลือกคอลัมน์ที่ต้องการแสดง:", options=all_cols, default=all_cols)

with ctrl_col3:
    sort_col = st.selectbox("เรียงข้อมูลตามคอลัมน์:", options=selected_cols if selected_cols else all_cols)
    sort_order = st.radio("ลำดับ:", options=["มากไปน้อย (Descending)", "น้อยไปมาก (Ascending)"], horizontal=True)

# Apply Column Selection
if selected_cols:
    df_show = df_display[selected_cols].copy()
else:
    df_show = df_display.copy()

# Apply Search
if search_query:
    query = search_query.strip().lower()
    mask = df_show.astype(str).apply(lambda row: row.str.lower().str.contains(query).any(), axis=1)
    df_show = df_show[mask]

# Apply Sorting
ascending_flag = (sort_order == "น้อยไปมาก (Ascending)")
if sort_col in df_show.columns:
    df_show = df_show.sort_values(by=sort_col, ascending=ascending_flag)

# -------------------------------------------------------------
# 4. Render Table & Metrics
# -------------------------------------------------------------
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric("จำนวนแถวทั้งหมด (Rows)", f"{len(df_show):,} แถว")
with m_col2:
    st.metric("จำนวนคอลัมน์ (Columns)", f"{len(df_show.columns):,} คอลัมน์")
with m_col3:
    if "net_sales" in df_show.columns:
        st.metric("ยอดขายรวมของตารางนี้", f"฿{df_show['net_sales'].sum():,.2f}")

st.dataframe(
    df_show,
    use_container_width=True,
    height=450
)

# -------------------------------------------------------------
# 5. Export Data Section
# -------------------------------------------------------------
st.markdown("### 📥 ดาวน์โหลดรายงานข้อมูล (Export CSV)")
csv_data = df_show.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')

st.download_button(
    label="⬇️ ดาวน์โหลดข้อมูลนี้เป็น CSV (รองรับภาษาไทยใน Excel)",
    data=csv_data,
    file_name=f"egg_tart_sales_{view_mode.split()[0]}.csv",
    mime="text/csv"
)

# -------------------------------------------------------------
# 6. Statistical Summary Section
# -------------------------------------------------------------
with st.expander("📊 สรุปสถิติเชิงตัวเลข (Numerical Summary & Describe)"):
    num_df = df_show.select_dtypes(include=['number'])
    if not num_df.empty:
        st.dataframe(num_df.describe().T, use_container_width=True)
    else:
        st.info("ไม่มีคอลัมน์เชิงตัวเลขในตารางที่เลือก")

render_footer()
