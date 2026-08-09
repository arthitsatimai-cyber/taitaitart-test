"""
UI Components and Styling Utilities for Tai Tai Tart Sales Dashboard
Handcrafted Custom Theme (Human Designer Aesthetic)
Palette: Warm Peach/Terracotta (#E07A5F), Sage Teal (#81B29A), Soft Sand (#FDFBF7)
"""

from datetime import datetime
import streamlit as st


def inject_custom_css():
    """Inject handcrafted human-designed CSS theme into Streamlit app."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Prompt:wght@300;400;500;600&display=swap');

        /* Global Typography & Soft Natural Background */
        html, body, [class*="css"], .stApp {
            font-family: 'Prompt', 'Plus Jakarta Sans', sans-serif !important;
            background: linear-gradient(135deg, #FDFBF7 0%, #F5EBE1 100%) !important;
            color: #33272A !important;
        }

        /* Sidebar Styling - Handcrafted Warm Cream feel */
        [data-testid="stSidebar"] {
            background: #FFFDF9 !important;
            border-right: 1px solid #EFE4D6 !important;
            box-shadow: 2px 0 12px rgba(92, 64, 51, 0.03);
        }

        [data-testid="stSidebar"] * {
            color: #4A3B32 !important;
        }

        /* Human Card Container Styling */
        .kpi-card {
            background: #FFFFFF;
            padding: 22px 24px;
            border-radius: 18px;
            box-shadow: 0 4px 20px -2px rgba(186, 117, 70, 0.08);
            border: 1px solid #F3E7DB;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .kpi-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px -4px rgba(186, 117, 70, 0.14);
            border-color: #E8D3C0;
        }

        .kpi-title {
            font-size: 13.5px;
            color: #8C7A6B;
            font-weight: 500;
            letter-spacing: 0.2px;
            margin-bottom: 8px;
        }

        .kpi-value {
            font-size: 28px;
            font-weight: 600;
            color: #3B2A1D;
            letter-spacing: -0.5px;
        }

        .kpi-badge {
            display: inline-block;
            background: #FDF4EC;
            color: #D97736;
            padding: 3px 9px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
            margin-top: 6px;
        }

        /* Custom Button Styling */
        .stButton>button {
            background: linear-gradient(135deg, #E07A5F 0%, #D96B4E 100%) !important;
            color: #FFFFFF !important;
            font-weight: 500 !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 10px 22px !important;
            box-shadow: 0 4px 12px rgba(224, 122, 95, 0.25) !important;
            transition: all 0.2s ease !important;
        }

        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 16px rgba(224, 122, 95, 0.35) !important;
            background: linear-gradient(135deg, #D96B4E 0%, #C85A3D 100%) !important;
        }

        /* Download Button Styling */
        .stDownloadButton>button {
            background: linear-gradient(135deg, #3D405B 0%, #2B2D42 100%) !important;
            color: #FFFFFF !important;
            font-weight: 500 !important;
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(43, 45, 66, 0.2) !important;
        }

        /* Custom Section Box */
        .content-card {
            background: #FFFFFF;
            padding: 26px 30px;
            border-radius: 20px;
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
            border: 1px solid #F0E5D8;
            margin-bottom: 24px;
        }

        /* Streamlit Tab Custom Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            height: 44px;
            white-space: pre;
            background-color: #F8F1E9;
            border-radius: 12px;
            color: #6C5B51;
            font-weight: 500;
            padding: 0 18px;
            border: 1px solid #EFE4D6;
        }

        .stTabs [aria-selected="true"] {
            background-color: #E07A5F !important;
            color: #FFFFFF !important;
            border-color: #E07A5F !important;
            font-weight: 600 !important;
        }

        /* Clean Hide Streamlit Chrome */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(title: str, subtitle: str, icon: str = "🥧"):
    """Render a styled human-crafted page header."""
    st.markdown(
        f"""
        <div class="content-card" style="border: 1px solid #F0E5D8; background: linear-gradient(135deg, #FFFFFF 0%, #FDFBF7 100%);">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="width: 56px; height: 56px; background: #FDF2E9; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 30px; border: 1px solid #F6DFD0;">
                    {icon}
                </div>
                <div>
                    <h1 style="color: #3B2A1D; font-weight: 600; font-size: 26px; margin: 0; letter-spacing: -0.3px;">{title}</h1>
                    <p style="color: #8C7A6B; font-size: 14.5px; margin: 4px 0 0 0; font-weight: 400;">{subtitle}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(title: str, value: str, icon: str, subtitle: str = ""):
    """Render a custom handcrafted KPI card."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div class="kpi-title">{title}</div>
                <span style="font-size: 24px; opacity: 0.85;">{icon}</span>
            </div>
            <div class="kpi-value">{value}</div>
            {"<div class='kpi-badge'>" + subtitle + "</div>" if subtitle else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    """Render subtle footer with developer team names."""
    current_date = datetime.now().strftime("%d/%m/%Y")
    st.markdown(
        f"""
        <div style="text-align: center; color: #A09083; font-size: 12.5px; padding: 24px 0 10px 0; font-weight: 400; line-height: 1.6;">
            Crafted for <b>Tai Tai Tart</b> | คณะผู้พัฒนา: <b>ทรงวุฒิ จิพิมาย, ณัฐวุฒิ แซ่ตั้ง, ชาริดา พัฒนคร้าย, กรวรรณ วงษ์งาม, อาทิตย์ สติใหม่</b><br>
            🗓️ อัปเดตล่าสุด: {current_date}
        </div>
        """,
        unsafe_allow_html=True,
    )

