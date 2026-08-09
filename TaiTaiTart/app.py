"""
Egg Tart Sales Dashboard - Home Page (app.py)
Developer: OriZaMa Channel
Theme: Warm Bakery (#F4A261, #F7D9C4, #FAF3E0)
"""

from datetime import datetime
import streamlit as st
from utils.components import inject_custom_css, render_footer, render_header

# Set Streamlit Page Config
st.set_page_config(
    page_title="ระบบวิเคราะห์ยอดขายร้าน Tai Tai Tart | Egg Tart Sales Dashboard",
    page_icon="🥧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Custom CSS Theme
inject_custom_css()

# Render Main Header
render_header(
    title="ระบบวิเคราะห์ยอดขายร้าน Tai Tai Tart",
    subtitle="Tai Tai Tart Sales Analysis Dashboard",
    icon="🥧",
)

# -------------------------------------------------------------
# 1. วัตถุประสงค์ของระบบ (System Objectives)
# -------------------------------------------------------------
st.markdown("### 🎯 วัตถุประสงค์ของระบบ (System Objectives)")
col_obj1, col_obj2 = st.columns(2)

with col_obj1:
    st.markdown(
        """
        <div class="kpi-card" style="text-align: center; padding: 20px;">
            <div style="font-size: 36px; margin-bottom: 8px;">🛍️</div>
            <div style="font-weight: 600; font-size: 18px; margin-bottom: 6px; color:#2B2D42;">เพื่อการสั่งซื้อที่สะดวก</div>
            <div style="font-size: 14px; color: #6C757D;">อำนวยความสะดวกให้ผู้ใช้และเจ้าของร้านสามารถจัดการและตรวจสอบรายการสั่งซื้อได้อย่างง่ายดายผ่านเว็บไซต์</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_obj2:
    st.markdown(
        """
        <div class="kpi-card" style="text-align: center; padding: 20px;">
            <div style="font-size: 36px; margin-bottom: 8px;">✨</div>
            <div style="font-weight: 600; font-size: 18px; margin-bottom: 6px; color:#2B2D42;">รับรู้เมนูใหม่ๆ ผ่านเว็บไซต์</div>
            <div style="font-size: 14px; color: #6C757D;">ช่วยให้ผู้ใช้งานสามารถติดตามและรับรู้ข่าวสารสินค้า เมนูทาร์ตไข่ใหม่ๆ ของร้านได้อย่างรวดเร็ว</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# -------------------------------------------------------------
# 2. เมนูสินค้าแนะนำ (Featured Egg Tart Menu)
# -------------------------------------------------------------
st.markdown("### 🥧 เมนูสินค้าทาร์ตไข่ Tai Tai Tart (Menu Products)")
p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns(5)

products_info = [
    ("ทาร์ตไข่ชาไทย", "🧋", "40 บาท", "รสชาไทยเข้มข้น หอมกลิ่นชาไทยแท้"),
    ("ทาร์ตไข่ชาเขียว", "🍵", "40 บาท", "มัทฉะพรีเมียม กลมกล่อมละมุนลิ้น"),
    ("ทาร์ตไข่คาราเมล", "🍯", "45 บาท", "หอมคาราเมลไหม้ หวานกำลังดี"),
    ("ทาร์ตไข่สตรอว์เบอร์รี่", "🍓", "50 บาท", "ตัดซอสสตรอว์เบอร์รี่สด เปรี้ยวหวานลงตัว"),
    ("ทาร์ตไข่ช็อกโกแลต", "🍫", "45 บาท", "เข้มข้นด้วยช็อกโกแลตแท้เต็มคำ"),
]

for col, (name, emoji, price, desc) in zip(
    [p_col1, p_col2, p_col3, p_col4, p_col5], products_info
):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card" style="text-align:center; padding:16px;">
                <div style="font-size:36px;">{emoji}</div>
                <div style="font-weight:700; font-size:15px; margin-top:6px; color:#2B2D42;">{name}</div>
                <div style="font-weight:600; font-size:14px; color:#F4A261;">{price}</div>
                <div style="font-size:12px; color:#6C757D; margin-top:4px;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

# -------------------------------------------------------------
# 3. คำอธิบายชุดข้อมูล & วิธีใช้งานโดยย่อ
# -------------------------------------------------------------
col_info, col_guide = st.columns(2)

with col_info:
    st.markdown(
        """
        <div class="content-card">
            <h3 style="color:#F4A261; margin-top:0;">📋 คำอธิบายชุดข้อมูล (Dataset Info)</h3>
            <p style="color:#2B2D42; line-height:1.7;">
                ข้อมูลการขายของร้าน <b>taitaitart</b> ซึ่งใช้สำหรับวิเคราะห์ยอดขายและพัฒนาแดชบอร์ดด้วยระบบ Streamlit 
                โดยข้อมูลแต่ละแถวแทนรายการสั่งซื้อ (Order) 1 รายการ ประกอบด้วยรายละเอียดของสินค้า จำนวนที่ซื้อ ราคา ส่วนลด 
                และวิธีการชำระเงิน เพื่อนำไปวิเคราะห์พฤติกรรมการซื้อของลูกค้าและผลการดำเนินงานของร้าน
            </p>
            <hr style="border: 0.5px solid #F0E6D8; margin: 12px 0;">
            <p style="font-weight:600; margin-bottom:6px;">คอลัมน์สำคัญในชุดข้อมูล:</p>
            <ul style="line-height: 1.8; color:#2B2D42; font-size:14px;">
                <li><b>order_id:</b> รหัสรายการสั่งซื้อ</li>
                <li><b>order_date:</b> วันที่สั่งซื้อ</li>
                <li><b>branch:</b> สาขาที่ขาย</li>
                <li><b>product_name:</b> ชื่อเมนูทาร์ตไข่</li>
                <li><b>quantity:</b> จำนวนที่ซื้อ</li>
                <li><b>unit_price:</b> ราคาต่อหน่วย</li>
                <li><b>discount_rate:</b> ส่วนลด</li>
                <li><b>payment_method:</b> วิธีการชำระเงิน</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col_guide:
    st.markdown(
        """
        <div class="content-card">
            <h3 style="color:#F4A261; margin-top:0;">💡 วิธีใช้งานโดยย่อ (Quick Guide)</h3>
            <ol style="line-height: 2.0; color:#2B2D42;">
                <li><b>เลือกข้อมูล:</b> เลือกใช้ข้อมูลตัวอย่าง หรือ อัปโหลดไฟล์ <code>.csv</code> / <code>.xlsx</code> ของคุณที่หน้า Dashboard</li>
                <li><b>กรองข้อมูล:</b> กรองข้อมูลตามช่วงวันที่, สาขา, เมนู, และวิธีการชำระเงิน</li>
                <li><b>วิเคราะห์ Dashboard:</b> ติดตามสรุป KPI รวม และกราฟวิเคราะห์ 4 มิติ</li>
                <li><b>สำรวจข้อมูล (Data Explorer):</b> ค้นหา กรอง คัดเลือกคอลัมน์ และเรียงลำดับข้อมูลดิบ</li>
                <li><b>ดาวน์โหลดรายงาน:</b> ส่งออกข้อมูลที่กรองแล้วเป็นไฟล์ CSV รองรับภาษาไทย</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------------------------------------
# 4. ผู้พัฒนาระบบ (Developer Team)
# -------------------------------------------------------------
st.markdown("### 👨‍💻 คณะผู้พัฒนาโครงงาน (Developer Team)")
st.markdown(
    """
    <div class="content-card">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; text-align: center;">
            <div style="background:#FDF8F3; padding:12px; border-radius:12px; border:1px solid #F6DFD0;">👨‍💻 <b>นายทรงวุฒิ จิพิมาย</b></div>
            <div style="background:#FDF8F3; padding:12px; border-radius:12px; border:1px solid #F6DFD0;">👨‍💻 <b>นายณัฐวุฒิ แซ่ตั้ง</b></div>
            <div style="background:#FDF8F3; padding:12px; border-radius:12px; border:1px solid #F6DFD0;">👩‍💻 <b>น.ส.ชาริดา พัฒนคร้าย</b></div>
            <div style="background:#FDF8F3; padding:12px; border-radius:12px; border:1px solid #F6DFD0;">👩‍💻 <b>น.ส.กรวรรณ วงษ์งาม</b></div>
            <div style="background:#FDF8F3; padding:12px; border-radius:12px; border:1px solid #F6DFD0;">👨‍💻 <b>นายอาทิตย์ สติใหม่</b></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Navigation Buttons Action
st.markdown("### 🚀 เริ่มต้นใช้งานระบบ")
nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    st.info("📊 ไปยังหน้า **Sales Dashboard** เพื่อวิเคราะห์ยอดขายและกราฟเปรียบเทียบ")

with nav_col2:
    st.success("📋 ไปยังหน้า **Data Explorer** เพื่อสำรวจ ค้นหา และดาวน์โหลดข้อมูล")

# Render Footer
render_footer()

