"""
Sales Dashboard Page - Egg Tart Sales Dashboard
Pages File: pages/1_Sales_Dashboard.py
Developer: OriZaMa Channel
"""

import streamlit as st
import pandas as pd
from utils.components import inject_custom_css, render_header, render_kpi_card, render_footer
from utils.data_utils import load_sample_data, load_uploaded_data, clean_data, filter_data
from utils.analytics import (
    calculate_kpis,
    get_daily_sales,
    get_sales_by_branch,
    get_top_products,
    get_sales_by_payment,
    generate_business_insights
)
from utils.charts import plot_daily_sales_line, plot_sales_by_branch_bar, plot_top_products_hbar, plot_payment_method_pie

st.set_page_config(
    page_title="Sales Dashboard | ระบบวิเคราะห์ยอดขายร้านขายทาร์ตไข่",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

render_header(
    title="📊 Sales Dashboard (วิเคราะห์ยอดขาย)",
    subtitle="รายงานสรุปยอดขาย, ตัวชี้วัดสำคัญ (KPIs), แผนภูมิวิเคราะห์ และการเปรียบเทียบกับเป้าหมาย",
    icon="📊"
)

# -------------------------------------------------------------
# 1. Sidebar - Data Source, Target Setting & Filters
# -------------------------------------------------------------
st.sidebar.markdown("## ⚙️ ตั้งค่า & ตัวกรองข้อมูล")

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
        st.info("ℹ️ กรุณาอัปโหลดไฟล์ CSV หรือ Excel ทาง Sidebar ซ้ายมือเพื่อเริ่มการวิเคราะห์")
        st.stop()

# Perform Data Cleaning
df_clean = clean_data(df_raw)

if df_clean.empty:
    st.warning("⚠️ ไม่พบข้อมูลหลังทำความสะอาด")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 ตั้งค่าเป้าหมายยอดขาย (Sales Target)")
target_sales_input = st.sidebar.number_input(
    "กำหนดเป้าหมายยอดขาย (บาท):",
    min_value=10000.0,
    max_value=1000000.0,
    value=150000.0,
    step=10000.0
)

st.sidebar.markdown("---")
with st.sidebar.expander("🔍 ตัวกรองข้อมูล (Filters)", expanded=True):
    # Date Filter
    min_date = df_clean['order_date'].min().date()
    max_date = df_clean['order_date'].max().date()
    
    selected_dates = st.date_input(
        "📅 เลือกช่วงวันที่:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Branch Filter
    branches = sorted(df_clean['branch'].unique().tolist())
    selected_branches = st.multiselect(
        "🏬 เลือกสาขา (Branch):",
        options=branches,
        default=branches
    )
    
    # Product Filter
    products = sorted(df_clean['product_name'].unique().tolist())
    selected_products = st.multiselect(
        "🥧 เลือกเมนูสินค้า (Products):",
        options=products,
        default=products
    )
    
    # Payment Filter
    payments = sorted(df_clean['payment_method'].unique().tolist())
    selected_payments = st.multiselect(
        "💳 เลือกวิธีชำระเงิน (Payment):",
        options=payments,
        default=payments
    )
    
    # Sales Range Slider
    min_sales_val = float(df_clean['net_sales'].min())
    max_sales_val = float(df_clean['net_sales'].max())
    
    sales_range = st.slider(
        "💰 ช่วงยอดขายสุทธิต่อรายการ (บาท):",
        min_value=round(min_sales_val, 0),
        max_value=round(max_sales_val, 0),
        value=(round(min_sales_val, 0), round(max_sales_val, 0))
    )

# Apply Filter
df_filtered = filter_data(
    df_clean,
    date_range=selected_dates if len(selected_dates) == 2 else None,
    selected_branches=selected_branches,
    selected_products=selected_products,
    selected_payments=selected_payments,
    sales_range=sales_range
)

if df_filtered.empty:
    st.error("❌ ไม่พบข้อมูลที่ตรงตามเงื่อนไขตัวกรองที่เลือก กรุณาปรับเปลี่ยนตัวกรองทางซ้ายมือ")
    st.stop()

# -------------------------------------------------------------
# 2. KPI Cards Section & Target Comparison
# -------------------------------------------------------------
kpis = calculate_kpis(df_filtered, target_sales=target_sales_input)

# Target Progress Bar Header
st.markdown("### 🎯 การเปรียบเทียบยอดขายกับเป้าหมาย (Sales vs Target Goal)")
t_col1, t_col2 = st.columns([3, 1])
with t_col1:
    progress_val = min(float(kpis['target_pct'] / 100), 1.0)
    st.progress(progress_val)
with t_col2:
    st.markdown(f"**ความคืบหน้า: `{kpis['target_pct']:.1f}%`** (เป้า: ฿{kpis['target_sales']:,.0f})")

st.write("")

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    render_kpi_card(
        title="ยอดขายสุทธิรวม",
        value=f"฿{kpis['total_sales']:,.2f}",
        icon="💰",
        subtitle=f"เทียบเป้าหมาย {kpis['target_pct']:.1f}%"
    )

with kpi_col2:
    render_kpi_card(
        title="จำนวนรายการขาย",
        value=f"{kpis['total_orders']:,} ออเดอร์",
        icon="🧾"
    )

with kpi_col3:
    render_kpi_card(
        title="จำนวนสินค้าขายได้",
        value=f"{kpis['total_units']:,} ชิ้น",
        icon="🥧"
    )

with kpi_col4:
    render_kpi_card(
        title="มูลค่าเฉลี่ย/ออเดอร์",
        value=f"฿{kpis['avg_order_value']:,.2f}",
        icon="📊"
    )

with kpi_col5:
    render_kpi_card(
        title="สินค้าขายดีสูงสุด",
        value=kpis['top_product'],
        icon="🏆",
        subtitle=f"ยอดขาย ฿{kpis['top_product_sales']:,.0f}"
    )

st.write("")

# -------------------------------------------------------------
# 3. Charts Section
# -------------------------------------------------------------
st.markdown("### 📊 แผนภูมิวิเคราะห์ยอดขาย (Visual Analytics)")

# Row 1 Charts: Daily Sales Line + Sales by Branch Bar
chart_row1_col1, chart_row1_col2 = st.columns([1.3, 1])

with chart_row1_col1:
    daily_sales_df = get_daily_sales(df_filtered)
    fig_daily = plot_daily_sales_line(daily_sales_df)
    st.pyplot(fig_daily, use_container_width=True)

with chart_row1_col2:
    branch_sales_df = get_sales_by_branch(df_filtered)
    fig_branch = plot_sales_by_branch_bar(branch_sales_df)
    st.pyplot(fig_branch, use_container_width=True)

st.write("")

# Row 2 Charts: Top 5 Products Horizontal Bar + Payment Method Pie
chart_row2_col1, chart_row2_col2 = st.columns([1.2, 1])

with chart_row2_col1:
    top_products_df = get_top_products(df_filtered, top_n=5)
    fig_top = plot_top_products_hbar(top_products_df)
    st.pyplot(fig_top, use_container_width=True)

with chart_row2_col2:
    payment_sales_df = get_sales_by_payment(df_filtered)
    fig_pay = plot_payment_method_pie(payment_sales_df)
    st.pyplot(fig_pay, use_container_width=True)

st.write("")

# -------------------------------------------------------------
# 4. Business Logic & Insights Section (คำอธิบายและการแปลผลเชิงธุรกิจ)
# -------------------------------------------------------------
st.markdown("### 💡 สรุปผลวิเคราะห์และการแปลผลเชิงธุรกิจ (Business Insights)")
insights = generate_business_insights(df_filtered, target_sales=target_sales_input)

with st.container():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    for insight in insights:
        st.markdown(f"- {insight}")
    st.markdown('</div>', unsafe_allow_html=True)

render_footer()

