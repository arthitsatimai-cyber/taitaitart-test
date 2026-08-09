# 🥧 ระบบวิเคราะห์ยอดขายร้านขายทาร์ตไข่ (Egg Tart Sales Dashboard)

แอปพลิเคชันเว็บสมบูรณ์สำหรับการวิเคราะห์ข้อมูลยอดขายและติดตามประสิทธิภาพการขายของร้านขายทาร์ตไข่ พัฒนาด้วย **Python**, **Streamlit**, **Pandas** และ **Matplotlib**

---

## 🎨 โทนสีและดีไซน์ (Theme)
- **Primary Color:** `#F4A261` (ส้มอุ่นเบเกอรี่)
- **Secondary Color:** `#F7D9C4` (พาสเทลพีช)
- **Background Color:** `#FAF3E0` (ครีมอุ่น)
- **Card Color:** `#FFFFFF` พร้อมเงาสมูท
- **Typography:** รองรับตัวอักษรภาษาไทย คลีน อ่านง่าย สบายตา

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```text
simple_sales_dashboard/
├── app.py                      # หน้าหลัก (Home Page)
├── pages/
│   ├── 1_Sales_Dashboard.py    # หน้า Dashboard วิเคราะห์ยอดขายและกราฟ
│   └── 2_Data_Explorer.py      # หน้าสำรวจ ค้นหา และดาวน์โหลดข้อมูล
├── utils/
│   ├── data_utils.py           # ฟังก์ชันโหลดข้อมูล ทำความสะอาด และกรองข้อมูล
│   ├── analytics.py            # ฟังก์ชันคำนวณ KPIs และสถิติ
│   ├── charts.py               # ฟังก์ชันวาดแผนภูมิ Matplotlib
│   └── components.py           # UI Components และ Custom CSS
├── data/
│   └── sample_sales.csv        # ชุดข้อมูลตัวอย่างยอดขาย (320 แถว)
├── requirements.txt            # รายการไลบรารีที่จำเป็น
└── README.md                   # คู่มือการติดตั้งและใช้งาน
```

---

## 🛠️ วิธีติดตั้งและใช้งาน (Installation & Run Guide)

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 2. รันโปรเจกต์ Streamlit Web App
```bash
streamlit run app.py
```

---

## 🥧 สินค้าและข้อมูลในระบบ (Product Information)
1. **ทาร์ตไข่ชาไทย** (40 บาท)
2. **ทาร์ตไข่ชาเขียว** (40 บาท)
3. **ทาร์ตไข่คาราเมล** (45 บาท)
4. **ทาร์ตไข่สตรอว์เบอร์รี่** (50 บาท)
5. **ทาร์ตไข่ช็อกโกแลต** (45 บาท)

### สาขา (Branches)
- Bangkok
- Chiang Mai
- Khon Kaen
- Phuket

---

## 👨‍💻 ข้อมูลผู้พัฒนา
- **ผู้พัฒนา:** OriZaMa Channel
- **ปรับปรุงล่าสุด:** ปัจจุบัน (Auto Updated)
