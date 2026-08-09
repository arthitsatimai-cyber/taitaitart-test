"""
Matplotlib Chart Generation Utilities with Custom Theme
Theme Palette:
- Primary: #F4A261 (Warm Orange)
- Accent Dark: #E76F51 (Terracotta)
- Accent Teal: #2A9D8F (Teal)
- Accent Yellow: #E9C46A (Sand Yellow)
- Secondary: #F7D9C4 (Soft Peach)
- Background: #FAF3E0
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import streamlit as st

# Configure matplotlib style
plt.rcParams['font.sans-serif'] = ['Prompt', 'Tahoma', 'Arial Unicode MS', 'Thonburi', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

PRIMARY_COLOR = '#E07A5F'      # Soft Terracotta/Warm Peach
ACCENT_COLOR = '#D96B4E'       # Muted Warm Rust
TEAL_COLOR = '#81B29A'         # Sage / Soft Mint Teal
YELLOW_COLOR = '#F4F1DE'       # Warm Cream / Sand
DARK_SLATE = '#3D405B'         # Deep Soft Slate
CARD_BG = '#FFFFFF'
TEXT_MAIN = '#3B2A1D'          # Deep Warm Charcoal
TEXT_MUTED = '#8C7A6B'         # Muted Warm Taupe
GRID_COLOR = '#F5EBE1'         # Very Soft Warm Grid

PALETTE = ['#E07A5F', '#81B29A', '#F2CC8F', '#3D405B', '#D96B4E', '#E8D3C0']


def apply_chart_style(fig, ax, title, xlabel, ylabel):
    """Apply elegant, subtle human-designer style to matplotlib figure and axes."""
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)
    
    ax.set_title(title, fontsize=13, fontweight=600, pad=18, color=TEXT_MAIN, loc='left')
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, labelpad=8, color=TEXT_MUTED)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, labelpad=8, color=TEXT_MUTED)
        
    ax.tick_params(colors=TEXT_MUTED, labelsize=9.5)
    ax.grid(True, linestyle='--', alpha=0.7, color=GRID_COLOR)
    
    # Hide top, right, and left spines for a clean minimal layout
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#EFE4D6')
    ax.spines['bottom'].set_linewidth(1.0)



def plot_daily_sales_line(daily_df: pd.DataFrame):
    """1. Line Chart: Daily Sales Trend (ยอดขายรายวัน)."""
    fig, ax = plt.subplots(figsize=(10, 4.5))
    
    if daily_df.empty:
        ax.text(0.5, 0.5, "ไม่มีข้อมูลสำหรับแสดงผล", ha='center', va='center', fontsize=12)
        return fig

    ax.plot(
        daily_df['order_date'], 
        daily_df['net_sales'], 
        color=PRIMARY_COLOR, 
        linewidth=2.5, 
        marker='o', 
        markersize=4,
        markerfacecolor=ACCENT_COLOR,
        markeredgecolor=ACCENT_COLOR
    )
    
    # Fill area under line
    ax.fill_between(
        daily_df['order_date'], 
        daily_df['net_sales'], 
        color=PRIMARY_COLOR, 
        alpha=0.15
    )
    
    apply_chart_style(
        fig, ax, 
        title="📈 แนวโน้มยอดขายรายวัน (Daily Sales Trend)", 
        xlabel="วันที่ (Date)", 
        ylabel="ยอดขายสุทธิ (บาท)"
    )
    
    # Format Y-axis as currency
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"฿{x:,.0f}"))
    fig.autofmt_xdate(rotation=30)
    plt.tight_layout()
    return fig


def plot_sales_by_branch_bar(branch_df: pd.DataFrame):
    """2. Bar Chart: Sales by Branch (ยอดขายแยกตามสาขา)."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    
    if branch_df.empty:
        ax.text(0.5, 0.5, "ไม่มีข้อมูลสำหรับแสดงผล", ha='center', va='center', fontsize=12)
        return fig

    bars = ax.bar(
        branch_df['branch'], 
        branch_df['net_sales'], 
        color=PALETTE[:len(branch_df)],
        width=0.55,
        edgecolor='#FFFFFF',
        linewidth=1.2
    )
    
    # Add value labels above bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f'฿{height:,.0f}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha='center', va='bottom',
            fontsize=9.5, fontweight='bold', color=TEXT_MAIN
        )

    apply_chart_style(
        fig, ax, 
        title="🏬 ยอดขายแยกตามสาขา (Sales by Branch)", 
        xlabel="สาขา (Branch)", 
        ylabel="ยอดขายสุทธิ (บาท)"
    )
    
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"฿{x:,.0f}"))
    plt.tight_layout()
    return fig


def plot_top_products_hbar(top_products_df: pd.DataFrame):
    """3. Horizontal Bar Chart: Top 5 Best-Selling Products (Top 5 สินค้าขายดี)."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    
    if top_products_df.empty:
        ax.text(0.5, 0.5, "ไม่มีข้อมูลสำหรับแสดงผล", ha='center', va='center', fontsize=12)
        return fig

    # Sort ascending for horizontal bar chart (top product at top)
    sorted_df = top_products_df.sort_values(by='net_sales', ascending=True)

    bars = ax.barh(
        sorted_df['product_name'], 
        sorted_df['net_sales'], 
        color=PRIMARY_COLOR,
        height=0.55,
        edgecolor=ACCENT_COLOR,
        linewidth=1.0
    )
    
    # Add labels on bars
    for bar in bars:
        width = bar.get_width()
        ax.annotate(
            f' ฿{width:,.0f}',
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(5, 0),
            textcoords="offset points",
            ha='left', va='center',
            fontsize=9.5, fontweight='bold', color=TEXT_MAIN
        )

    apply_chart_style(
        fig, ax, 
        title="🏆 5 อันดับสินค้าขายดีที่สุด (Top 5 Best-Selling Products)", 
        xlabel="ยอดขายสุทธิ (บาท)", 
        ylabel="ชื่อเมนูทาร์ตไข่"
    )
    
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"฿{x:,.0f}"))
    plt.tight_layout()
    return fig


def plot_payment_method_pie(payment_df: pd.DataFrame):
    """4. Pie Chart: Payment Method Breakdown (สัดส่วนการชำระเงิน)."""
    fig, ax = plt.subplots(figsize=(6, 4.5))
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)
    
    if payment_df.empty:
        ax.text(0.5, 0.5, "ไม่มีข้อมูลสำหรับแสดงผล", ha='center', va='center', fontsize=12)
        return fig

    colors = [TEAL_COLOR, PRIMARY_COLOR, ACCENT_COLOR, YELLOW_COLOR]
    
    wedges, texts, autotexts = ax.pie(
        payment_df['net_sales'],
        labels=payment_df['payment_method'],
        autopct='%1.1f%%',
        startangle=140,
        colors=colors[:len(payment_df)],
        textprops=dict(color=TEXT_MAIN, fontsize=10),
        wedgeprops=dict(width=0.45, edgecolor='#FFFFFF', linewidth=2)  # Donut style
    )

    for autotext in autotexts:
        autotext.set_color('#FFFFFF')
        autotext.set_weight('bold')
        autotext.set_fontsize(10)

    ax.set_title("💳 สัดส่วนการชำระเงิน (Payment Method Breakdown)", fontsize=13, fontweight='bold', color=TEXT_MAIN, pad=15)
    plt.tight_layout()
    return fig
